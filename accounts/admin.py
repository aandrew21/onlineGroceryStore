from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # If using a custom user model

admin.site.register(CustomUser, UserAdmin)
# Register your models here.
