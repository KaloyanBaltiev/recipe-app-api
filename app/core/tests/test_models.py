"""
Tests for models.
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_new_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected_email in sample_emails:
            user = get_user_model().objects.create_user(email, 'password123')
            self.assertEqual(user.email, expected_email)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'password123')

    def test_create_super_user(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'superuser@example.com',
            'password123'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_recipe(self):
        """Test creating a new recipe is successful."""
        user = get_user_model().objects.create_user(
            'testuser@example.com',
            'testpass123',
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Simple Recipe name',
            time_minutes=5,
            price=Decimal('5.50'),
            description='Simple Recipe Description',
        )
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)
