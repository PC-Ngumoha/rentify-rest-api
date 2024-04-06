"""
Creating custom models for the API
"""
from django.contrib.auth.models import (
  AbstractBaseUser,
  PermissionsMixin,
  BaseUserManager
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Custom user model manager"""

    def create_user(self, email, password=None, **extra):
        """Create, save & return a new user."""
        if not email:
            raise ValueError(_('Email field is REQUIRED'))
        user = self.model(
            email=self.normalize_email(email),
            **extra
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        """Create, save & return a new superuser."""
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User DB model"""
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        """String representation"""
        return self.email


class Country(models.Model):
    """Country DB model"""
    name = models.CharField(unique=True)

    def __str__(self):
        return self.name


class PropertyType(models.Model):
    """Property types"""
    name = models.CharField(unique=True)

    def __str__(self):
        return self.name


class Unit(models.Model):
    """Unit of time for renting properties"""
    DAY = 'DAY'
    WEEK = 'WEEK'
    MONTH = 'MONTH'
    YEAR = 'YEAR'
    UNIT_CHOICES = [
        (DAY, 'Day'),
        (WEEK, 'Week'),
        (MONTH, 'Month'),
        (YEAR, 'Year'),
    ]
    name = models.CharField(max_length=20,
                            choices=UNIT_CHOICES,
                            default=MONTH)

    def __str__(self):
        return self.name
