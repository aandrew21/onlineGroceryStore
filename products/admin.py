from django.contrib import admin
from .models import Product  # ✅ Add this line if missing

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock')  # Adjust fields based on your model
    search_fields = ('name',)

admin.site.register(Product, ProductAdmin)

