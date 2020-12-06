from django.contrib.auth.models import User
from django.db import models
import time


class Employee(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=30)
    employee_id = models.CharField(max_length=10, default='0')
    employee_time = models.CharField(max_length=10, default=time.strftime("%Y-%m-%d", time.localtime()))
    nine = models.FloatField(default=0)
    ten = models.FloatField(default=0)
    eleven = models.FloatField(default=0)
    twelve = models.FloatField(default=0)
    thirteen = models.FloatField(default=0)
    fourteen = models.FloatField(default=0)
    fifteen = models.FloatField(default=0)
    sixteen = models.FloatField(default=0)
    seventeen = models.FloatField(default=0)
    eighteen = models.FloatField(default=0)
    nineteen = models.FloatField(default=0)
    twenty = models.FloatField(default=0)
    twentyOne = models.FloatField(default=0)
    twentyTwo = models.FloatField(default=0)
    twentyThree = models.FloatField(default=0)
    twentyFour = models.FloatField(default=0)
    time = models.CharField(max_length=10, default=time.strftime("%Y-%m-%d", time.localtime()))

    objects = models.Manager()

    def __str__(self):
        return self.inventory_name
