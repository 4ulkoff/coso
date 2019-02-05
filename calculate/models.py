from django.db import models



from catalog.models import Product
from django.contrib.auth.models import User





# Create your models here.




class Set(models.Model):
    class Meta:
        verbose_name = 'Набор'
        verbose_name_plural = 'Ноборы'
        ordering = ('id',)

    TYPE = (
        (0, 'Анулирован'),
        (1, 'Активeн'),
        (2, 'Закрыт'),
        (3, 'Выполнен'),
    )

    status = models.SmallIntegerField(choices=TYPE, default=1, db_index=True, verbose_name='Статус')
    title = models.CharField(max_length=300, null=True, blank=True, verbose_name='Наименование')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    
    user = models.ForeignKey(User, verbose_name='Пользователь', db_index=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s' % (self.title)

class SetList(models.Model):
    
    class Meta:
        verbose_name = 'Компоненты набора'
        verbose_name_plural = 'Компоненты наборов'
        
    set = models.ForeignKey('Set', verbose_name='Набор', db_index=True, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, verbose_name='Продукт', db_index=True, on_delete=models.SET_NULL, null=True)
    
    value = models.IntegerField(default=1, verbose_name='Количество', help_text='Объём закупаемого товара')
    order = models.IntegerField(default=0, verbose_name='Порядок')

    def __str__(self):
        return '%s(%s)' % (Set.pk, Product.title)

class ActivSet(models.Model):

    class Meta:
        verbose_name = 'Активный набор' #Комплект
        verbose_name_plural = 'Активные наборы'

    user = models.ForeignKey(User, verbose_name='Продукт', db_index=True, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, verbose_name='Продукт', db_index=True, on_delete=models.SET_NULL, null=True)

    value = models.IntegerField(default=1, verbose_name='Количество', help_text='Объём закупаемого товара')
    order = models.IntegerField(default=0, verbose_name='Порядок')

    def __str__(self):
        return '%s' % (Product.title)

