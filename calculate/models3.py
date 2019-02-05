from django.db import models



from catalog.models import Product
from django.contrib.auth.models import User





# Create your models here.



class Set(models.Model):
    class Meta:
        verbose_name = 'Набор'
        verbose_name_plural = 'Ноборы'
        ordering = ('id',)

    title = models.CharField(max_length=300, null=True, blank=True, verbose_name='Наименование')

class SetUser(models.Model):
    class Meta:
        verbose_name = 'Набор пользователя'
        verbose_name_plural = 'Ноборы  пользователей'
        ordering = ('id',)

    title = models.CharField(max_length=300, null=True, blank=True, verbose_name='Наименование')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    comment = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Комментарий',
                               help_text="Комментарии специалистов для внутреннего пользования")
    set = models.ForeignKey('Set', verbose_name='Сборка', db_index=True, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', db_index=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s' % (self.title)

class SetList(models.Model):
    class Meta:
        verbose_name = 'Компоненты сборки'
        verbose_name_plural = 'Компоненты сборок'
        ordering = ('id',)

    set = models.ForeignKey('Set', verbose_name='Сборка', db_index=True, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, verbose_name='Продукт', db_index=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s(%s)' % (Set.id, Product.title)

class ActivSet(models.Model):

    class Meta:
        verbose_name = 'Активный набор' #Комплект
        verbose_name_plural = 'Активные наборы'

    user = models.ForeignKey(User, verbose_name='Продукт', db_index=True, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, verbose_name='Продукт', db_index=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s' % (Product.title)

