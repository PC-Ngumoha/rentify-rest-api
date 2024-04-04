"""
Tests for all the models used in the app.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase

from parameterized import parameterized


class TestModels(TestCase):
    """Testing DB models"""

    def test_create_user(self):
        """Tests that we can create normal user."""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testing123#'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Tests that we can create super user."""
        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='testing123#'
        )
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    @parameterized.expand([
        ('test1@EXAMPLE.com', 'test1@example.com'),
        ('Test2@Example.com', 'Test2@example.com'),
        ('TEST3@EXAMPLE.COM', 'TEST3@example.com'),
        ('test4@example.com', 'test4@example.com'),
    ])
    def test_email_normalized(self, input, expected, cipher='testing123'):
        """Tests that email is normalized on user creation."""
        user = get_user_model().objects.create_user(
            email=input,
            password=cipher
        )
        self.assertEqual(user.email, expected)
