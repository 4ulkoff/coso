from django.db import models
from django.utils import timezone

from catalog.models import Product, Category



class Distr(models.Model):

    CAT_TYPE = (
        (0, 'Не активно'),
        (1, 'Активно'),
        (2, 'Заблокировано'),

    )

    type = models.SmallIntegerField(choices=CAT_TYPE, default=1, db_index=True, verbose_name='Тип', help_text='Тип дистрибьютора')
    distr = models.CharField(max_length=200, verbose_name='Дистрибьютор', help_text="Наименование дистрибьютора")
    alias = models.CharField(max_length=200, blank=True, verbose_name='Псевдоним', help_text="Псевдоним используется для официальных названий или указания головы")
    url = models.URLField(max_length=300, blank=True, verbose_name='Ссылка', help_text="Ссылка на сайт дистрибьютора")
    img = models.ImageField(max_length=100, blank=True, verbose_name='Лого', help_text="Логотип дистрибьютора (Желательно SVG)")

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s (%s)' % (self.distr, self.alias)


    class Meta:
        verbose_name = 'Дистрибьютор'

class Code(models.Model):

    TYPE = (
        (0, 'Не активно'),
        (1, 'Активно'),
        (2, 'Заблокировано'),

    )

    type = models.SmallIntegerField(choices=TYPE, default=1, db_index=True, verbose_name='Тип', help_text='Тип')
    code = models.CharField(max_length=200, verbose_name='Код', help_text="Код дистрибьютора")
    distr = models.ForeignKey('Distr', verbose_name='Дистрибьютор', db_index=True, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, verbose_name='Продукт', db_index=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s (%s)' % (self.distr, Product.title)


    class Meta:
        verbose_name = 'Код дистрибьютора'

class ExceptCode(models.Model):
    class Meta:
        verbose_name = 'Исключённый код'
        verbose_name_plural = 'Исключённые коды'
        permissions = (("except_code", "Исключать код"),)

    TYPE = (
        (0, 'Не активно'),
        (1, 'Активно'),
        (2, 'Заблокировано'),

    )

    type = models.SmallIntegerField(choices=TYPE, default=1, db_index=True, verbose_name='Тип', help_text='Тип')
    code = models.CharField(max_length=200, verbose_name='Код', help_text="Исключаемый код дистрибьютора")
    description = models.TextField(blank=True, null=True, verbose_name='Описание', help_text="Описние")
    comment = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Комментарий',
                               help_text="Комментарии специалистов для внутреннего пользования")

    distr = models.ForeignKey('Distr', verbose_name='Дистрибьютор', db_index=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s (%s)' % (self.code, self.distr)

class DistrCategory(models.Model):
    class Meta:
        verbose_name = 'Категория дистрибьютора'
        verbose_name_plural = 'Категории дистрибьютора'

    TYPE = (
        (0, 'Неактивна'),
        (1, 'Активная'),
        (2, 'Заблокированна'),
        (3, 'Новая'),
    )

    type = models.SmallIntegerField(choices=TYPE, default=2, db_index=True, verbose_name='Тип', help_text='Тип')
    name = models.CharField(max_length=300, verbose_name='Категрия', help_text="Наименование категории дистрибьютора")
    category = models.ForeignKey(Category, verbose_name='Категория', default=10, db_index=True, null=True, on_delete=models.SET_NULL,)
    distr = models.ForeignKey('Distr', verbose_name='Дистрибьютор', db_index=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s (%s)' % (self.name, self.category)

class Currency(models.Model):
    class Meta:
        verbose_name = 'Котировка'
        verbose_name_plural = 'Котировки'

    SYMBOL = (
        (0, 'Неизвестно'),
        (1, 'USD'),
    )

    symbol = models.SmallIntegerField(choices=SYMBOL, default=1, db_index=True, verbose_name='Валюта', help_text='Банковский символ валюты')
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Котировка')
    date = models.DateField(verbose_name='Дата')

    def __str__(self):
        return '%s (%s)' % (self.rate, self.date)

class DistrCurrency(models.Model):
    class Meta:
        verbose_name = 'Котировка'
        verbose_name_plural = 'Котировки'

    SYMBOL = (
        (0, 'Неизвестно'),
        (1, 'USD'),
    )

    symbol = models.SmallIntegerField(choices=SYMBOL, default=1, db_index=True, verbose_name='Валюта',
                                      help_text='Банковский символ валюты')
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Котировка')
    date = models.DateField(verbose_name='Дата')
    distr = models.ForeignKey('Distr', verbose_name='Дистрибьютор', db_index=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s (%s) - %s' % (self.rate, self.date, self.distr)

class Price(models.Model):
    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'

    TYPE = (
        (0, 'Устарела'),
        (1, 'Актуальная'),
    )

    type = models.SmallIntegerField(choices=TYPE, default=1, db_index=True, verbose_name='Тип', help_text='Тип')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Оптовая цена')
    retail = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Розничная цена')
    date = models.DateTimeField(verbose_name='Дата')

    distr = models.ForeignKey('Distr', verbose_name='Дистрибьютор', db_index=True, on_delete=models.SET_NULL, null=True)
    code = models.ForeignKey('Code', verbose_name='Код дистрибьютора', db_index=True, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, verbose_name='Продукт', db_index=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s - %s(%s)' % (self.price, self.distr, Product.title)

class Stock(models.Model):
    class Meta:
        verbose_name = 'Остатки'
        verbose_name_plural = 'Остатки'

    TYPE = (
        (0, 'Устарели'),
        (1, 'Актуальны'),
    )
    VAR = (
        (0, ''),
        (1, '<'),
        (2, '>'),
    )

    type = models.SmallIntegerField(choices=TYPE, default=1, db_index=True, verbose_name='Тип', help_text='Тип')
    var = models.SmallIntegerField(choices=VAR, default=0, verbose_name='Примерно', help_text='Больще/меньше')
    value = models.IntegerField(null=True, blank=True, verbose_name='Объёмы', help_text='Остатки на складе')
    date = models.DateTimeField(verbose_name='Дата')

    distr = models.ForeignKey('Distr', verbose_name='Дистрибьютор', db_index=True, on_delete=models.SET_NULL, null=True)
    code = models.ForeignKey('Code', verbose_name='Код дистрибьютора', db_index=True, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, verbose_name='Продукт', db_index=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s %s' % (self.var, self.value)

class DistrFile(models.Model):
    class Meta:
        verbose_name = 'Прайс-лист'
        verbose_name_plural = 'Прайс-листы'

    TYPE = (
        (0, 'Анулирован'),
        (1, 'Обработан'),
        (2, 'В обработке'),
        (3, 'Ожидает'),
    )

    type = models.SmallIntegerField(choices=TYPE, default=2, db_index=True, verbose_name='Тип', help_text='Тип')
    date = models.DateTimeField(default=timezone.now, null=True, blank=True, verbose_name='Дата', help_text="Дата прайса")
    count = models.IntegerField(null=True, blank=True, verbose_name='Позиции', help_text="Количество позиций")
    count_new = models.IntegerField(null=True, blank=True, verbose_name='Новые позиции', help_text="Количество новых позиций")
    file = models.FileField(upload_to='price',verbose_name='Файл', help_text="Файл с прайсом")
    distr = models.ForeignKey('Distr', verbose_name='Дистрибьютор', db_index=True, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '%s (%s)' % (self.file, self.date)


class Forex(models.Model):
    ask = models.FloatField()
    bid = models.FloatField()
    time = models.DateTimeField()

class Matrix(models.Model):
    point = models.IntegerField()
    time = models.IntegerField()












