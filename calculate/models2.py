from django.db import models



from catalog.models import Product
from django.contrib.auth.models import User





# Create your models here.

class SetType(models.Model):
    class Meta:
        verbose_name = 'Тип сборки'
        verbose_name_plural = 'Типы сборки'
        ordering = ('title',)

    title = models.CharField(max_length=200, null=True, blank=True, verbose_name='Наименование')

    def __str__(self):
        return '%s' % (self.title)


class Set(models.Model):
    class Meta:
        verbose_name = 'Сборка'
        verbose_name_plural = 'Сборки'
        ordering = ('id',)

    type = models.ForeignKey('SetType', default=1, verbose_name='Тип', db_index=True, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=300, null=True, blank=True, verbose_name='Наименование')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    comment = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Комментарий',
                               help_text="Комментарии специалистов для внутреннего пользования")

    def __str__(self):
        return '%s' % (self.title)

class SetList(models.Model):
    class Meta:
        verbose_name = 'Компоненты сборки'
        verbose_name_plural = 'Компоненты сборок'
        ordering = ('id',)

    set = models.ForeignKey('Set', verbose_name='Сборка', db_index=True, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, verbose_name='Продукт', db_index=True, on_delete=models.SET_NULL, null=True)
    order = models.SmallIntegerField(default=0, blank=True, null=True, verbose_name='Порядок')

    def __str__(self):
        return '%s' % (Set.title)



class SetUser(models.Model):
    class Meta:
        verbose_name = 'Набор пользователя' #Комплект
        verbose_name_plural = 'Наборы пользователей'
        ordering = ('id',)

    TYPE = (
        (0, 'Анулированно'),
        (1, 'Активно'),
        (2, 'Архив'),
    )

    status = models.SmallIntegerField(choices=TYPE, default=1, db_index=True, verbose_name='Статус')
    set = models.ForeignKey('Set', verbose_name='Сборка', db_index=True, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, verbose_name='Продукт', db_index=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s' % (Set.title)


class ActivSet(models.Model):

    class Meta:
        verbose_name = 'Активный набор' #Комплект
        verbose_name_plural = 'Активные наборы'

    user = models.ForeignKey(User, verbose_name='Продукт', db_index=True, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, verbose_name='Продукт', db_index=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s' % (Product.title)
