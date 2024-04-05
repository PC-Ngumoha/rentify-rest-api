"""
Unit tests for User creation and management A.P.I.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
LOGIN_USER_URL = reverse('user:login')
ME_URL = reverse('user:me')


def create_user(**params):
    """Helper function: create user for test purposes."""
    return get_user_model().objects.create_user(**params)


class TestUserAPIPublicTests(TestCase):
    """Unauthenticated Tests for the user API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        """Tests that user can be created successfully."""
        payload = {
            'email': 'test@example.com',
            'password': 'testing123',
            'name': 'Sample User',
        }
        res = self.client.post(CREATE_USER_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload.get('email'))
        self.assertTrue(user.check_password(payload.get('password')))
        self.assertNotIn('password', res.data)

    def test_not_create_user_without_correct_payload(self):
        """Tests that user cannot be created with incorrectly formatted
        data.
        """
        payload = {
            'email': 'test@example.com',
        }
        res = self.client.post(CREATE_USER_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_create_user_with_duplicate_email(self):
        """Tests that user cannot be created twice with the same email.
        """
        payload = {
            'email': 'test@example.com',
            'password': 'testing123'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_login_user_non_existing(self):
        """Tests that we cannot login as non-existent user."""
        payload = {
            'email': 'test@example.com',
            'password': 'testing123'
        }
        res = self.client.post(LOGIN_USER_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_fail_with_bad_data(self):
        """Tests that login should fail if data is incorrectly formatted.
        """
        payload = {
            'email': 'test@example.com',
        }
        res = self.client.post(LOGIN_USER_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_successfully(self):
        """Tests that we should be able to login successfully."""
        payload = {
            'email': 'test@example.com',
            'password': 'testing123'
        }
        create_user(**payload)
        res = self.client.post(LOGIN_USER_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_unable_to_retrieve_user_unauthenticated(self):
        """Tests that unauthenticated users are unable to retrieve a profile.
        """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class TestUserAPIPrivateTests(TestCase):
    """Authenticated tests for the user API endpoints"""

    def setUp(self):
        self.client = APIClient()
        payload = {
            'email': 'test@example.com',
            'password': 'testing123',
            'name': 'Test User',
        }
        user = create_user(**payload)
        self.client.force_authenticate(user=user)

    def test_me_endpoint_post_method_unallowed(self):
        """Tests that POST does not work on the me/ endpoint.
        """
        payload = {
            'email': 'test@example.com',
        }
        res = self.client.post(ME_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_able_to_retrieve_user_authenticated(self):
        """Tests that authenticated user is able to retrieve profile.
        """
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(res.data)
        self.assertIn('email', res.data)
        self.assertNotIn('password', res.data)

    def test_able_to_update_profile(self):
        """Tests that authenticated user is able to update profile.
        """
        update_payload = {
            'email': 'tested@example.com',
            'name': 'Gift'
        }
        patch_res = self.client.patch(ME_URL, data=update_payload)

        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)

        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get('name'), update_payload.get('name'))
