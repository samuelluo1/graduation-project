from django.db import models


# Create your models here.
class Item(models.Model):

    item_name = models.CharField(max_length=20, verbose_name='品項名稱')
    item_price = models.CharField(max_length=10, verbose_name='品項價格', null=True, blank=True)
    time = models.CharField(max_length=10, verbose_name='製作時間', null=True, blank=True)
    sales = models.CharField(max_length=10, verbose_name='售出量', null=True, blank=True)

    class Meta:
        verbose_name = '菜單品項'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.item_name


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=20, verbose_name='原物料名稱')
    ingredient_price = models.CharField(max_length=10, verbose_name='原物料價格', null=True, blank=True)

    class Meta:
        verbose_name = '食品原物料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ingredient_name


class Have(models.Model):
    proportion = models.CharField(max_length=10, verbose_name='比例', null=True, blank=True)
    item = models.ForeignKey(Item, default='',  on_delete=models.CASCADE, verbose_name='菜單品項')
    ingredient = models.ForeignKey(Ingredient, default='',  on_delete=models.CASCADE, verbose_name='食品原物料')

    class Meta:
        verbose_name = '菜單原物料關聯'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.proportion


class Miscellaneous(models.Model):
    miscellaneous_name = models.CharField(max_length=20, verbose_name='人事雜項名稱')
    miscellaneous_price = models.CharField(max_length=10, verbose_name='人事雜項花費', null=True, blank=True)
    service = models.CharField(max_length=10, verbose_name='服務作業比例', null=True, blank=True)
    cooking = models.CharField(max_length=10, verbose_name='料理作業比例', null=True, blank=True)
    sorting = models.CharField(max_length=10, verbose_name='整理管理比例', null=True, blank=True)

    class Meta:
        verbose_name = '人事雜項'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.miscellaneous_name
