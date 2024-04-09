"""
URL patterns for the listing API
"""
from django.urls import path

from listing import views

app_name = 'listing'

urlpatterns = [
  path('property_types/', views.PropertyTypeListingView.as_view(),
       name='property_types'),
  path('countries/', views.CountryListingView.as_view(), name='countries'),
  path('locations/', views.LocationListingView.as_view(), name='locations'),
  path('amenities/', views.AmenityListingView.as_view(), name='amenities'),
]
