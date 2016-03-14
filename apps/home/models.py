"""Models for home app.

It contains Product model.
"""

from django.db import models
from django.template.defaultfilters import slugify


class Product(models.Model):
    """Model for Product.

    It store product details of search item after scraping in database.
    """

    # Char fields.
    name = models.CharField(max_length=255, null=True, blank=True)
    product_type = models.CharField(max_length=30, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    site_reference = models.CharField(max_length=50, null=True, blank=True)

    # Float field.
    price = models.FloatField(default=0.0, null=True, blank=True)

    # DateTime Field.
    scraped_date = models.DateTimeField(auto_now=True, auto_now_add=False)

    # URL field.
    landing_url = models.URLField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    slug_name = models.SlugField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        """To save slug_name which is slugified form of name field."""
        self.slug_name = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        """Value to return if object is called."""
        return self.name
