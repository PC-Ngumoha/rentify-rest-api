"""
URL patterns for user API
"""
from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
  path('create/', views.CreateUserView.as_view(), name='create'),
  path('login/', views.LoginUserView.as_view(), name='login'),
  path('me/', views.RetrieveUpdateUserView.as_view(), name='me')
]
