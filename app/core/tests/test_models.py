from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='haris@baabte.com', password='12345'):
    """
    Create a sample user for the test
    """
    return get_user_model().objects.create_user(email, password)


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
        user = get_user_model().objects.create_superuser(
                        "test@test.com",
                        'test123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """
        Test the tag representation
        """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Nonvegan'
            )
        self.assertEqual(str(tag), tag.name)
