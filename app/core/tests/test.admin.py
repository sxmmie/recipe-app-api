from django.test import TestCase
from django.test import Client  # allows us make test request to our app unittest
from django.urls import reverse  # generate urls for admin page
from django.contrib.auth import get_user_model


# Admin page unittest
class AdminSiteTests(TestCase):

    # setup function/task, runs before any test runs.
    # consists of creating test client, add new user for testing, make sure user is logged into the client,
    # create a regular user that is not authenticated
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='samuelumohjnr@gmail.com',
            password='Eden0189??'
        )
        # Uses the Client helper function that allows for logging a  user in with the django authentication.
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='samoski93@gmail.com',
            password='hacker123',
            name='Test user full name'
        )

        # Test that users are listed in the django admin
        def test_users_listed(self):
            """Test that users are listed on user page"""
            url = reverse('admin:core_user_changelist')
            res = self.client.get(url)

            self.assertContains(res, self.user.name)
            self.assertContains(res, self.user.email)

        # test that change page renders correctly
        def test_user_change_page(self):
            """test that the user edit page works"""
            url = reverse('admin:core_user_change', args=[
                          self.user.id])  # /admin/core/user/id
            res = self.client.get(url)

            self.assertContains(res.status_code, 200)

        # test that add page renders correctly
        def test_create_user_page(self):
            """Test that the create user edit page works"""
            url = reverse('admin:core_user_add')
            res = self.client.get(url)

            self.assertEqual(res.status_code, 200)
