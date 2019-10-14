from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@gmail.com', password='testpass'):
    """Helper function to create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@gmail.com'
        password = 'password1'
        # create_user() is from the UserManager
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        # run assertions to make sure user was created correctly
        self.assertEqual(user.email, email)
        # password is encrypted, so use the password_check() from the django user model.
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        """Test the email for a new user is normalized"""
        email = 'test1@gmail.com'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    # validation to ensure that an email field is actually been provided when the create_user() function is called.
    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test234')

    # create_superuser() is used to create new user using the django cli.
    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@gmail.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    # create a tag and verifies that it converts to the correct string representation
    def test_tag_str(self):
        """Test tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    # Test to see that the ingredient model exists and we can create and retrieve the model
    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    # Create recipe and return as a string
    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    # mock the uuid library that comes by default with python, change the value it returns
    # Anytime the uuid4() is called (triggered from inside this function), we change the return value
    @patch('uuid.uuid4')
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that test is saved in the correct location"""
        uuid = 'test uuid'
        mock_uuid.return_value = uuid
        file_path = models.recipe_image_file_path(None, myimage.jpg)

        exp_path = f'upload/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
