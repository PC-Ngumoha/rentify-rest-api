"""
Contains the tests for the listing API
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    PropertyType,
    Country,
    Location,
)
from listing.serializers import (
    PropertyTypeSerializer,
    CountrySerializer,
    LocationSerializer,
)

TYPES_URL = reverse('listing:property_types')
COUNTRIES_URL = reverse('listing:countries')
LOCATIONS_URL = reverse('listing:locations')


def create_user(**params):
    """Handles creating new users for testing"""
    return get_user_model().objects.create_user(**params)


class TestListingAPIPublicTests(TestCase):
    """Tests unauthenticated requests made to the API"""

    def setUp(self):
        self.client = APIClient()

    def test_property_type_list_request(self):
        """Tests unauthenticated requests to list all property types available
        """
        property_types = ('Bungalow', 'Duplex', 'Cottage', 'Chatteau')
        for property_type in property_types:
            PropertyType.objects.create(
                name=property_type
            )
        res = self.client.get(TYPES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        property_types = PropertyType.objects.all()
        serializer = PropertyTypeSerializer(property_types, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_country_list_request(self):
        """Tests unauthenticated requests to list all countries available.
        """
        countries = ('Nigeria', 'Ghana', 'South Africa', 'Malawi', 'Gabon')
        for country_name in countries:
            Country.objects.create(
                name=country_name
            )
        res = self.client.get(COUNTRIES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_location_list_request(self):
        """Test listing all locations available."""
        country1 = Country.objects.create(name='Nigeria')
        country2 = Country.objects.create(name='Canada')
        nig_locations = ('Kubwa', 'Bwari', 'Pangshin, Jos', 'Jos city',
                         'Kaduna city')
        cd_locations = ('Winnipeg, Manitoba', 'Ontario', 'Montreal')
        for location_name in nig_locations:
            Location.objects.create(
                name=location_name,
                country=country1
            )
        for location_name in cd_locations:
            Location.objects.create(
                name=location_name,
                country=country2
            )
        res = self.client.get(LOCATIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_location_list_request_filter_by_country(self):
        """Test listing locations belonging to a specific country."""
        country1 = Country.objects.create(name='Nigeria')
        country2 = Country.objects.create(name='Canada')
        nig_locations = ('Kubwa', 'Bwari', 'Pangshin, Jos', 'Jos city',
                         'Kaduna city')
        cd_locations = ('Winnipeg, Manitoba', 'Ontario', 'Montreal')
        for location_name in nig_locations:
            Location.objects.create(
                name=location_name,
                country=country1
            )
        for location_name in cd_locations:
            Location.objects.create(
                name=location_name,
                country=country2
            )
        res = self.client.get(LOCATIONS_URL, {'country': 'Nigeria'})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        l1 = Location.objects.filter(country=country1)
        l2 = Location.objects.filter(country=country2)
        s1 = CountrySerializer(l1, many=True)
        s2 = CountrySerializer(l2, many=True)
        self.assertEqual(res.data, s1.data)
        self.assertNotEqual(res.data, s2.data)


class TestListingAPIPrivateTests(TestCase):
    """Tests authenticated requests made to the API"""

    def setUp(self):
        payload = {
            'email': 'test@example.com',
            'password': 'testing123',
            'name': 'Test User'
        }
        user = create_user(**payload)
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_nothing(self):
        """Placeholder test"""
        pass
