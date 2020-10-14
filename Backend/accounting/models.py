from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=30)
    item_price = models.FloatField(default=0)
    time = models.FloatField(default=0)
    sales = models.FloatField(default=0)
    item_time = models.CharField(max_length=7)

    objects = models.Manager()

    def __str__(self):
        return self.item_name


class Ingredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient_name = models.CharField(max_length=30)
    ingredient_price = models.FloatField(default=0)
    ingredient_time = models.CharField(max_length=7)

    objects = models.Manager()

    def __str__(self):
        return self.ingredient_name


class Have(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    proportion = models.FloatField(default=0)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return self.proportion


class Miscellaneous(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    miscellaneous_name = models.CharField(max_length=30)
    miscellaneous_price = models.FloatField(default=0)
    service = models.FloatField(default=0)
    cooking = models.FloatField(default=0)
    sorting = models.FloatField(default=0)
    miscellaneous_time = models.CharField(max_length=7)

    objects = models.Manager()

    def __str__(self):
        return self.miscellaneous_name
