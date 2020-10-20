from django.contrib.auth.models import User
from django.db import models
import time


class Inventory(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    inventory_name = models.CharField(max_length=30)
    inventory_date = models.CharField(max_length=10, default=time.strftime("%Y-%m-%d", time.localtime()))
    inventory_quantity = models.FloatField(default=0)
    inventory_unitPrice = models.FloatField(default=0)

    objects = models.Manager()

    def __str__(self):
        return self.inventory_name
