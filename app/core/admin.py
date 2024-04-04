"""
Registering the project DB models in the app admin.
"""
from django.contrib import admin

from core import models

admin.site.register(models.User)
