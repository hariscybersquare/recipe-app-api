from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@test.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
            )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_emailnormalized(self):
        """Test the email id to find out if the email is normalized"""
        email = 'test@TEST2.COM'
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """
        Trying to create a user with no email will create an error.
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_super_user(self):
        """
        Test cases to check if the create super user is working fine.
        """
        user = get_user_model().objects.create_super_user(
                        "test@test.com",
                        'test123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
