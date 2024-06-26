"""
Contains all the API views for handling listings
"""
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from core.models import (
    PropertyType,
    Country,
    Location,
    Amenity,
)
from listing.serializers import (
    PropertyTypeSerializer,
    CountrySerializer,
    LocationSerializer,
    AmenitySerializer,
)


class PropertyTypeListingView(ListAPIView):
    """Handles the listing of all property types available."""
    queryset = PropertyType.objects.all()
    serializer_class = PropertyTypeSerializer


class CountryListingView(ListAPIView):
    """Handles the listing of all countries available"""
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class LocationListingView(ListAPIView):
    """Handles the listing of all locations available"""
    serializer_class = LocationSerializer

    def get_queryset(self):
        queryset = Location.objects.all()
        country_name = self.request.query_params.get('country')
        if country_name is not None:
            country = Country.objects.get(name=country_name.title())
            queryset = queryset.filter(country=country)
        return queryset


class AmenityListingView(ListAPIView):
    """Handles the listing of all amenities available."""
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer


class PropertyViewset(ModelViewSet):
    """Handles all the actions associated with properties"""
    pass
