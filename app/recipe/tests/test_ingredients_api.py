from django.contrib.auth import get_user_model
from django.urls import reverse # for generating the url
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

fromm core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')

class PublicIngredientApiTest(TestCase):
    """Test the publicly available API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required ti=o access the endpoint"""
        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateIngredientApiTest(TestCase):
    """Test the Private ingredient API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass'
        )
        self.client.for_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test retrieving a list of ingredients"""
        Ingredients.objects.create(user=self.user, name='Maggi')
        Ingredients.objects.create(user=self.user, name='Salt')

        # make request
        res = self.client.get(INGREDIENT_URL)

        # make sure response matches what we expect
        # retrieve all ingredients, serialize them and compare that the serialized ingredient matches the ingredients
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # test that the ingredients are limited the authenticated user
    def test_ingredients_limited_to_user(self):
        """Test that ingredients for the authenticated user is returned"""
        user2 = get_user_model().objects.create_user(
            'test@gmail.com',
            'tepsil'
        )
        Ingredient.objects.create(user=user2, name='Vinegar')   # assigned the object to the user

        ingredient = Ingredient.objects.create(user=self.user, name='Tumeric')

        res = self.client(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)  # just one result for authenticated user
        self.assertEqual(res.data[0]['name'], ingredient.name)
