from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import recipe
from recipe.serializers import RecipeSerializer

RECIPE_URL = reverse('recipe:recipe:list')

# helper function, easily create test sample recipes


def sample_recipe(user, **params):
    """Create and return a sample recipe"""
    defaults = {
        'title': 'Sample recipe',
        'time_minutes': 10,
        'price': 5.00
    }

    # update() helps overwrite the values the dict keys, or create the keys if they don't exists
    defaults.update(params)

    Recipe.objects.create(user=user, **defaults)


class PublicRecipeApiTests(TestCase):
    """Test public recipe API access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(RECIPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_AUTHORIZED)


class PrivateRecipeApiTests(TestCase):
    """Test unauthentictaed API access"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'yestpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipe.objects.all().order_by('id')
        serializer = RecipeSerializer(recipes, Many=True)
        self.assertEqual(res.status_code, status.HTTP_200_Ok)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_to_user(self):
        """Test retrieving recipes for user"""
        user2 = get_user_model().objects.create_user(
            'test@gmail.com',
            'testpass123'
        )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)

        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, Many=True)
        self.assertEqual(res.status_code, status.HTTP_200_Ok)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
