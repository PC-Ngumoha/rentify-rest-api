"""
Creating custom models for the API
"""
from django.contrib.auth.models import (
  AbstractBaseUser,
  PermissionsMixin,
  BaseUserManager
)
from django.conf import settings
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


class Amenity(models.Model):
    """Amenities available at the rented property"""
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    """Location of the property to be rented"""
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Property(models.Model):
    """The property to be rented"""
    name = models.CharField(max_length=255)
    price_per_unit = models.DecimalField(max_digits=5, decimal_places=2)
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        help_text=_('user that posted the listing.')
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        help_text=_('current location of the property.')
    )
    property_type = models.ForeignKey(
        PropertyType,
        on_delete=models.CASCADE,
        help_text=_('type of apartment being rented')
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        help_text=_('days, weeks, months when property is unavailable.')
    )

    def __str__(self):
        return self.name
