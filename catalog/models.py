from django.db import models
# from PIL import Image

import random

# Create your models here.

class Category(models.Model):

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name', )

    CAT_TYPE = (
        (0, 'Не активно'),
        (1, 'Активно'),
        (2, 'Заблокировано'),

    )

    type = models.SmallIntegerField(choices=CAT_TYPE, default=1, db_index=True, verbose_name='Тип', help_text='Тип категории')
    name = models.CharField(max_length=200, verbose_name='Категория', help_text="Наименование категории")
    alias = models.CharField(max_length=200, blank=True, verbose_name='Псевдоним', help_text="Псевдоним используется для профессионализмов, жаргона, сокращений и т.д. (CPU, RAM, HDD...)")
    img = models.ImageField(max_length=100, blank=True, verbose_name='Картинка', help_text="Картинка соответствующая категории")

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s' % (self.name)






class Vendor(models.Model):
    class Meta:
        verbose_name = 'Вендор'
        verbose_name_plural = 'Вендоры'
        ordering = ('vendor', )

    TYPE = (
        (0, 'Не активно'),
        (1, 'Активно'),
        (2, 'Заблокировано'),

    )

    type = models.SmallIntegerField(choices=TYPE, default=1, db_index=True, verbose_name='Тип', help_text='Тип')
    vendor = models.CharField(max_length=200, verbose_name='Вендор', help_text="Наименование производителя")
    alias = models.CharField(max_length=200, blank=True, verbose_name='Псевдоним', help_text="Псевдоним используется для сокращений и русских названий")
    url = models.URLField(max_length=300, blank=True, verbose_name='Ссылка', help_text="Ссылка на сайт производителя")
    img = models.ImageField(max_length=100, blank=True, verbose_name='Картинка', help_text="Логотип производителя")


    def __str__(self):
        """
            String for representing the Model object.
        """
        return '%s' % (self.vendor)





class Product(models.Model):
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('id',)

    TYPE = (
        (0, 'Не активно'),
        (1, 'Активно'),
        (2, 'Заблокировано'),
    )

    type = models.SmallIntegerField(choices=TYPE, default=1, db_index=True, verbose_name='Тип', help_text='Тип')
    number = models.IntegerField(unique=True, verbose_name='Нумерация', help_text='Уникальный код товара')

    # set = models.SmallIntegerField(default=0, verbose_name='Сет', help_text='Временно')
    iarticle = models.CharField(max_length=200, null=True, blank=True, verbose_name='Артикул тех.', help_text="Заводской или внутренний артикул")
    article = models.CharField(max_length=200, null=True, blank=True, verbose_name='Артикул', help_text="Артикул товара")
    title = models.CharField(max_length=300, null=True, blank=True, verbose_name='Заголовок', help_text="Заголовок состоит из: Категория Вендор Артикул")
    name = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Название', help_text="Полное название с краткими характеристиками")
    alias = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Псевдоним', help_text="Техническое название с краткими характеристиками")
    description = models.TextField(blank=True, null=True, verbose_name='Описание', help_text="Описние с подробными характеристиками")
    comment = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Комментарий', help_text="Комментарии специалистов для внутреннего пользования")
    url = models.URLField(max_length=500, null=True, blank=True, verbose_name='Ссылка', help_text="Ссылка на сайте производителя")
    img = models.ImageField(max_length=100, blank=True, null=True, verbose_name='Картинка', help_text="Картинка спродукта")
    category = models.ForeignKey('Category', verbose_name='Категория', db_index=True, on_delete=models.SET_NULL, null=True)
    vendor = models.ForeignKey('Vendor', verbose_name='Вендор', db_index=True, on_delete=models.SET_NULL, null=True)

    def set_number(self):
        nocode = False
        while nocode == False:
            number = random.randint(100000, 999999)
            pro = Product.objects.filter(number=number)
            if not pro:
                nocode = True
        return number

    def __str__(self):
        return '%s' % (self.title)

#

