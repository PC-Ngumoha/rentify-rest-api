"""
Tests for all the models used in the app.
"""
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from parameterized import parameterized

from core.models import (
    Country,
    PropertyType,
    Unit,
    Amenity,
    Location
)


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

    def test_country_db_model(self):
        """Tests the Country DB model"""
        countries = ('Nigeria', 'Venezuela', 'Ghana')
        for country in countries:
            Country.objects.create(
                name=country
            )
        self.assertEqual(Country.objects.all().count(), len(countries))
        country = Country.objects.get(name=countries[0])
        self.assertEqual(country.name, str(country))

    def test_country_must_be_unique(self):
        """Tests that an instance of Country must be unique"""
        Country.objects.create(
            name='Nigeria'
        )
        with self.assertRaises(IntegrityError):
            Country.objects.create(
                name='Nigeria'
            )

    def test_property_type_db_model(self):
        """Tests the PropertyType DB model"""
        property_types = ('Bungalow', 'Duplex', 'Cottage')
        for property_type in property_types:
            PropertyType.objects.create(
                name=property_type
            )
        self.assertEqual(PropertyType.objects.all().count(),
                         len(property_types))
        property_type = PropertyType.objects.get(name=property_types[0])
        self.assertEqual(property_type.name, str(property_type))

    def test_property_type_must_be_unique(self):
        """Tests that all property types added to DB are unique."""
        PropertyType.objects.create(
            name='Bungalow'
        )
        with self.assertRaises(IntegrityError):
            PropertyType.objects.create(
                name='Bungalow'
            )

    def test_unit_db_model_with_valid_units(self):
        """Tests that we can set units correctly"""
        unit_choice = 'DAY'
        unit = Unit.objects.create(
            name=unit_choice
        )
        self.assertEqual(unit.name, unit_choice)

    def test_unit_db_model_default_is_month(self):
        """Tests that a unit is set to Month by default when created."""
        unit = Unit.objects.create()
        self.assertEqual(unit.name, Unit.MONTH)

    def test_amenity_db_model(self):
        """Tests for the Amenity DB model"""
        amenities = ('Wifi', 'Swimming pool', 'Gym')
        for amenity_name in amenities:
            Amenity.objects.create(
                name=amenity_name
            )
        self.assertEqual(Amenity.objects.all().count(), len(amenities))
        amenity = Amenity.objects.get(name=amenities[0])
        self.assertEqual(amenity.name, str(amenity))

    def test_amenity_must_be_unique(self):
        """Tests that instances of the Amenity model must be unique."""
        Amenity.objects.create(
            name='Wifi'
        )
        with self.assertRaises(IntegrityError):
            Amenity.objects.create(
                name='Wifi'
            )

    def test_location_db_model(self):
        """Tests the Location DB model"""
        country = Country.objects.create(name='Nigeria')
        location_names = ('Ebute Metta', 'Enugu', 'Awka Avenue')
        for location_name in location_names:
            Location.objects.create(
                name=location_name,
                country=country
            )
        self.assertEqual(Location.objects.all().count(), len(location_names))
        location = Location.objects.get(name=location_names[0])
        self.assertEqual(location.name, str(location))
