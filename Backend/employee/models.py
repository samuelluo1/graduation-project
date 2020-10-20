from django.contrib.auth.models import User
from django.db import models
import time


class Employee(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    employee_name = models.CharField(max_length=30)
    employee_id = models.FloatField(max_length=10, default=0)
    employee_time = models.CharField(max_length=10, default=time.strftime("%Y-%m-%d", time.localtime()))
    nine_f = models.FloatField(default=0)
    nine_s = models.FloatField(default=0)
    ten_f = models.FloatField(default=0)
    ten_s = models.FloatField(default=0)
    eleven_f = models.FloatField(default=0)
    eleven_s = models.FloatField(default=0)
    twelve_f = models.FloatField(default=0)
    twelve_s = models.FloatField(default=0)
    thirteen_f = models.FloatField(default=0)
    thirteen_s = models.FloatField(default=0)
    fourteen_f = models.FloatField(default=0)
    fourteen_s = models.FloatField(default=0)
    fifteen_f = models.FloatField(default=0)
    fifteen_s = models.FloatField(default=0)
    sixteen_f = models.FloatField(default=0)
    sixteen_s = models.FloatField(default=0)
    seventeen_f = models.FloatField(default=0)
    seventeen_s = models.FloatField(default=0)
    eighteen_f = models.FloatField(default=0)
    eighteen_s = models.FloatField(default=0)
    nineteen_f = models.FloatField(default=0)
    nineteen_s = models.FloatField(default=0)
    twenty_f = models.FloatField(default=0)
    twenty_s = models.FloatField(default=0)
    twentyOne_f = models.FloatField(default=0)
    twentyOne_s = models.FloatField(default=0)
    twentyTwo_f = models.FloatField(default=0)
    twentyTwo_s = models.FloatField(default=0)
    twentyThree_f = models.FloatField(default=0)
    twentyThree_s = models.FloatField(default=0)
    twentyFour_f = models.FloatField(default=0)
    twentyFour_s = models.FloatField(default=0)

    objects = models.Manager()

    def __str__(self):
        return self.inventory_name
