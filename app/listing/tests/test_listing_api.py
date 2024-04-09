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
    Amenity,
    Property,
    Unit,
)
from listing.serializers import (
    PropertyTypeSerializer,
    CountrySerializer,
    LocationSerializer,
    AmenitySerializer,
    PropertySerializer,
    PropertyDetailSerializer,
)

TYPES_URL = reverse('listing:property_types')
COUNTRIES_URL = reverse('listing:countries')
LOCATIONS_URL = reverse('listing:locations')
AMENITIES_URL = reverse('listing:amenities')
PROPERTY_LISTING_URL = reverse('listing:property-list')


def property_detail_url(prop_id):
    """Reverse url for the detail URL"""
    return reverse('listing:property-detail', args=[prop_id])


def create_user(**params):
    """Handles creating new users for testing"""
    return get_user_model().objects.create_user(**params)


def create_property(user, **params):
    """Handles creating useful Property objects"""
    payload = {
        "name": "Garden Heights",
        "price_per_unit": 34.56,
        "location": "Crescent moon street, Ekpe, Lagos",
        "country": "Nigeria",
        "property_type": "Bungalow",
        "unit": "DAY"
    }
    payload.update(**params)
    unit = Unit.objects.create(name=payload.pop('unit'))
    property_type = PropertyType.objects.create(
        name=payload.pop('property_type')
    )
    country = Country.objects.create(name=payload.pop('country'))
    location = Location.objects.create(
        name=payload.pop('location'),
        country=country
    )

    return Property.objects.create(
        user=user,
        location=location,
        property_type=property_type,
        unit=unit,
        **payload
    )


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

    def test_amenity_list_request(self):
        """Tests request to list all available Amenities."""
        amenities = ('Wifi', 'Swimming pool', 'Gym')
        for amenity_name in amenities:
            Amenity.objects.create(
                name=amenity_name
            )
        res = self.client.get(AMENITIES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        amenities = Amenity.objects.all()
        serializer = AmenitySerializer(amenities, many=True)
        self.assertEqual(res.data, serializer.data)


class TestListingAPIPrivateTests(TestCase):
    """Tests authenticated requests made to the API"""

    def setUp(self):
        payload = {
            'email': 'test@example.com',
            'password': 'testing123',
            'name': 'Test User'
        }
        self.user = create_user(**payload)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_property_requests(self):
        """Tests creating property requests"""
        payload = {
            "name": "Garden Heights",
            "price_per_unit": 34.56,
            "location": "Crescent moon street, Ekpe, Lagos",
            "country": "Nigeria",
            "property_type": "Bungalow",
            "unit": "DAY"
        }
        res = self.client.post(PROPERTY_LISTING_URL, data=payload,
                               format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        properties = Property.objects.all()
        self.assertIsNotNone(properties)
        self.assertNotEqual(properties, [])

    def test_list_property_requests(self):
        """Tests listing out all the properties available."""
        names = ('Richardson estate', 'Colonial avenue', 'Empty beach')
        prices = (23.45, 21.90, 34.56)
        for name, price in zip(names, prices):
            create_property(self.user, {
                'name': name,
                'price_per_unit': price,
            })

        res = self.client.get(PROPERTY_LISTING_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIs(type(res.data), list)
        properties = Property.objects.all()
        serializer = PropertySerializer(properties, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_property_requests(self):
        """Tests retrieving property requests"""
        prop = create_property(self.user, {
            'name': 'Garden towers resort, Ajah, Lagos',
            'price_per_unit': 21.37,
        })
        url = property_detail_url(prop.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = PropertyDetailSerializer(prop)
        self.assertEqual(res.data, serializer.data)

    def test_update_property_requests(self):
        """Tests updating property requests"""
        pass

    def test_delete_property_requests(self):
        """Tests deleting property requests"""
        pass
