from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


# constant url for the user to be tested
# user/create/ url assigned to the constant
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


# helper function used to create example users for our test
def create_user(**params):
    """pass"""
    return get_user_model().objects.create_user(**params)


class PublicUsersApiTests(TestCase):
    """Test users API (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Validate that user is created successfully (with valid payload)"""
        # payload is the object the user pass to the API when the request is made
        payload = {
            'email': 'test@gmail.com',
            'password': 'testpass',
            'name': 'test name'
        }
        # created user as response(res)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)  # get the created user
        # check password if true
        self.assertTrue(user.check_password(payload['password']))
        # check password not returned as part of object
        self.assertNotIn('password', res.data)

    # test for already existing user
    def test_user_exist(self):
        """Test creating a user that already exist fails"""
        payload = {'email': 'test@gmail.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 character"""
        payload = {'email': 'test@gmail.com', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    # Token Auth
    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test@gmail.com', 'password': 'tetpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        # the assertion test that there is a key called token inside the data
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@gmail.com', password='testpass')
        payload = {'email': 'test@gmail.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doesn't exist"""
        payload = {'email': 'test@gmail.com', 'password': 'tetpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserTests(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        """Setup authentication for test"""
        self.user = create_user(
            email='test@gmail.com',
            password='hacker',
            name='test'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    # Test that we can retrieve the profile of the authenticated user
    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # test the user object returned is what is expected
        self.assertEqual({
            'email': self.user.email,
            'name': self.user.name
        })

    def test_post_me_not_allowed(self):
        """Test that POST is not allowed on the me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user"""
        payload = {'name': 'new name', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
