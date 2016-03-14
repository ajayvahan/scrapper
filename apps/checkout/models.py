"""Model for checkout app.

It contains model of DeliveryDetail.
"""

from django.db import models
from django.contrib.auth.models import User
from apps.home.models import Product


class DeliveryDetail(models.Model):
    """Model for storing the details of the order.

    The billing address, user id, product id.
    """

    # ForeignKey relation with auth_user table
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,)

    # Char fields.
    order_id = models.CharField(max_length=20, blank=True)
    name = models.CharField(max_length=254, null=True, blank=True)
    address = models.CharField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)

    # Date field.
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    # Integer field.
    quantity = models.IntegerField(default=1)

    # Float field
    price = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        """To save total as product of quantity and price."""
        self.total = self.quantity * self.price
        super(DeliveryDetail, self).save(*args, **kwargs)

    def __str__(self):
        """Value to return if object is called."""
        return self.order_id
