"""
Contains all the serializers used for the project.
"""
from rest_framework import serializers


class PropertyTypeSerializer(serializers.Serializer):
    """Serializes instances of the PropertyType model"""
    name = serializers.CharField()


class CountrySerializer(serializers.Serializer):
    """Serializes instances of the Country model"""
    name = serializers.CharField()


class LocationSerializer(serializers.Serializer):
    """Serializes instances of the Location model"""
    name = serializers.CharField()
