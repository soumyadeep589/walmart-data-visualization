from django.db import models
from django.contrib.postgres.indexes import GinIndex

# Create your models here.

class Product(models.Model):
    product_id = models.CharField(max_length=255)
    name = models.CharField(max_length=250)
    previous_price = models.DecimalField(max_digits=10, decimal_places=4)
    display_price = models.DecimalField(max_digits=10, decimal_places=4)
    is_out_of_stock = models.BooleanField()
    is_active = models.BooleanField(default=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        db_table = "product"
        verbose_name_plural = "products"
        ordering = ["id"]
        indexes = [GinIndex(fields=['name'])]

    def __str__(self):
        return f"{self.id}, product_id: {self.product_id}, name: {self.name}"