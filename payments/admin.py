from django.contrib import admin
# Remove the import of Product
from products.models import Category  # Keep only necessary imports

admin.site.register(Category)  # Register only relevant models for payments

