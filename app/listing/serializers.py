"""
Contains all the serializers used for the project.
"""
from rest_framework import serializers

from core.models import (
    Unit,
    Property,
)


class PropertyTypeSerializer(serializers.Serializer):
    """Serializes instances of the PropertyType model"""
    name = serializers.CharField()


class CountrySerializer(serializers.Serializer):
    """Serializes instances of the Country model"""
    name = serializers.CharField()


class LocationSerializer(serializers.Serializer):
    """Serializes instances of the Location model"""
    name = serializers.CharField()


class AmenitySerializer(serializers.Serializer):
    """Serializes instances of the Amenity model"""
    name = serializers.CharField()


class UnitSerializer(serializers.Serializer):
    """Serializes the unit values"""
    name = serializers.ChoiceField(choices=Unit.UNIT_CHOICES)


class PropertySerializer(serializers.ModelSerializer):
    """Serializes the property detail summary for listing."""
    property_type = PropertyTypeSerializer()

    class Meta:
        model = Property
        fields = ['id', 'name', 'price_per_unit', 'available',
                  'property_type']


class PropertyDetailSerializer(PropertySerializer):
    """Serializes more details for a property."""
    country = CountrySerializer()
    location = LocationSerializer()
    unit = UnitSerializer()

    class Meta:
        fields = PropertySerializer.Meta.fields + ['country', 'location',
                                                   'unit']
        extra_kwargs = {
            'country': {
                'write_only': True,
                'required': False,
            },
        }

    def create(self, validated_data):
        """Creates an instance of the Property from serializer"""
        # unit_str = validated_data.pop('unit')
        # type_str = validated_data.pop('property_type')
        # country_str = validated_data.pop('country')
        # location_str = validated_data.pop('location')
        pass
