"""
Tests for all the models used in the app.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase


class TestModels(TestCase):
    """Testing DB models"""

    def test_create_user(self):
        """Testing that we can create normal user."""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testing123#'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Testing that we can create super user."""
        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='testing123#'
        )
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
