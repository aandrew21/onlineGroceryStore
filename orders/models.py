from django.db import models
from django.conf import settings
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')],
        default='Pending'
    )

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"

    def update_total(self):
        """Update the total price of the order."""
        total = sum(item.total_price for item in self.items.all())
        self.total_price = total
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        """Calculate the total price of the order item."""
        return self.product.price * self.quantity

