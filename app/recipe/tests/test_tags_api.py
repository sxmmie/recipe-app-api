from django.contrib.auth import get_user_model
from django.urls import reverse  # for generating the url
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer


# using a viewset, append the action make to the end of the url
TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient

    # test login required
    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# Authenticated test
class PrivateTagsApiTest(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        """Setup for authenticated user"""
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'passwordtest'
        )

        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        # sample tags
        Tag.objects.create(user=self.user, name='Vegan')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)  # http get to the url

        # make query to the model that we expected to get to the result
        # (result returned in alphabetical/reversed order based on name)
        tags = Tag.objects.all().order_by('-name')
        # many=True serializes a list of object
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # tags assigned to the authenticated user
    def test_tags_limited_user(self):
        """Test that tags returned are for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'othertest'
        )
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # expects only 1 result as only one tag was assigned to the user
        self.assertEqual(len(res.data), 1)
        # the name of in tag in res.data should equal that of the tag.name assigned to user
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {'name': 'Simple'}
        self.client.post(TAGS_URL, payload)

        # verify that user exists
        # filter all tags with the user that is the authenticated user and the name created in the test payload
        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    # creating a tag with an invalid name
    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
