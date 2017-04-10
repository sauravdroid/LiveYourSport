from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class Product(models.Model):
    ORDER_STATUS_CHOICE = (
        ('Active', 'Active'),
        ('Cancelled', 'Cancelled')
    )
    order_id = models.CharField(max_length=64, unique=True)
    order_status = models.CharField(max_length=64,choices=ORDER_STATUS_CHOICE)
    product_code = models.CharField(max_length=64)
    product_name = models.TextField()
    product_url = models.TextField()
    cost_price = models.FloatField(null=True)

    def __str__(self):
        return "Product " + str(
            self.pk) + '-->' + self.order_id + " " + self.order_status + " " + self.product_name + "  " + self.product_code + " "

    def get_rupee(self):
        if self.cost_price is not None:
            return self.cost_price * 66
        else:
            return None


class UploadedCSV(models.Model):
    filename = models.CharField(max_length=64, unique=True)
    csv_file = models.FileField()

    def __str__(self):
        return self.filename


class ScrapedCSV(models.Model):
    created_at = models.DateTimeField(default=timezone.now())
    csv_file = models.FileField()
