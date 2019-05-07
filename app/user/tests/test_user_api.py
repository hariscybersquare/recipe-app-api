from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
CREATE_TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """
    Create user needs to be called multiple times from the test cases.
    """
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """
    Tests the user API public.
    """
    def setUp(self):
        self.client = APIClient()

    def test_create_user_valid_success(self):
        """
        The user is created with a valid payload successfully.
        """
        payload = {
            'email': 'harisnew@baabte.com',
            'password': '12345',
            'name': 'Haris NP'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**res.data)

        self.assertEqual(user.email, 'harisnew@baabte.com')
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """
        The above functions tests if a user already existing is created or not.
        """
        payload = {
            'email': 'harisnew1@baabte.com',
            'password': '123456',
            'name': 'Haris NP - Existing'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Test that the password should be more than 5 characters.
        """
        payload = {
            'email': 'harisnew1@baabte.com',
            'password': '1234',
            'name': 'Haris NP - Existing'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
            ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """
        Test if the token created successfully.
        """
        payload = {
            'email': 'harisnew1@baabte.com',
            'password': '12345'
        }
        create_user(**payload)
        res = self.client.post(CREATE_TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_password(self):
        """
        Test invalid username and password response when
        wrong password is given.
        """
        payload = {
            'email': 'harisnew1@baabte.com',
            'password': '12345',
            'name': 'Haris NP - Existing'
        }
        create_user(**payload)
        res = self.client.post(CREATE_TOKEN_URL, {
            'email': 'harisnew1@baabte.com',
            'password': '123456'})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test__create_token_nonexisting_user(self):
        """
        Test for the non existing user
        """
        payload = {
            'email': 'harisnew1@baabte.com',
            'password': '12345',
            'name': 'Haris NP - Existing'
        }
        create_user(**payload)
        res = self.client.post(CREATE_TOKEN_URL, {
            'email': 'harisnewwe1@baabte.com',
            'password': '123456'})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test__create_token_no_password_passed(self):
        """
        Test for the no password passed.
        """
        payload = {
            'email': 'harisnew1@baabte.com',
            'password': '12345',
            'name': 'Haris NP - Existing'
        }
        create_user(**payload)
        res = self.client.post(CREATE_TOKEN_URL, {
            'email': 'harisnewwe1@baabte.com'})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """
        Tests if we are able to call the user details retrieve service
        without authentication
        """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """
    Test cases for the authenticated user requests
    """
    def setUp(self):
        self.user = create_user(
            email='haris@baabte.com',
            password='12345',
            name='Haris NP'
            )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """
        Test retrieving the profile for the logged in user.
        """
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
            })

    def test_post_me_not_allowed(self):
        """
        Tests if posts are allowed on the ME_URL
        """
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """
        Test if the user profile is udpated
        """
        payload = {'name': 'new name', 'password': 'harisnew'}

        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
