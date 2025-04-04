from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'status', 'total_price', 'created_at']
    search_fields = ['user__username', 'status']


# Register your models here.
