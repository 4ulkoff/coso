from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

# ========================

class Member(models.Model):
    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
        ordering = ('title', )

    TYPE = (
        (0, 'Неопределено'),
        (1, 'Персона'),
        (2, 'Организация'),
    )
    SEX = (
        (0, 'Неопределен'),
        (1, 'Мужской'),
        (2, 'Женский'),
    )

    type = models.SmallIntegerField(choices=TYPE, default=1, db_index=True, verbose_name='Тип', help_text='Тип участника')
    sex = models.SmallIntegerField(choices=SEX, default=0, db_index=True, verbose_name='Пол', help_text='Пол участника')

    title = models.CharField(max_length=200, verbose_name='Наименование', help_text="Обрвщене к участнику")
    surname = models.CharField(max_length=200, blank=True, verbose_name='Фамилия')
    name = models.CharField(max_length=200, blank=True, verbose_name='Имя')
    patronymic = models.CharField(max_length=200, blank=True, verbose_name='Отчество')
    registration = models.DateTimeField(default=timezone.now, null=True, blank=True, verbose_name='Дата регистрации')

    def __str__(self):
        return '%s' % (self.title)

class Email(models.Model):
    class Meta:
        verbose_name = 'E-mail'

    TYPE = (
        (0, 'Не активен'),
        (1, 'Основной'),
        (2, 'Дополнительный'),
    )

    type = models.SmallIntegerField(choices=TYPE, default=1, db_index=True, verbose_name='Тип', help_text='Тип контакта')
    email = models.EmailField(verbose_name='E-mail')

    member = models.ForeignKey('Member', verbose_name='Участник', on_delete=models.PROTECT)

    def __str__(self):
        return '%s' % (self.email)

class Phone(models.Model):
    class Meta:
        verbose_name = 'Телефон'
        verbose_name_plural = 'Телефоны'

    TYPE = (
        (0, 'Не активен'),
        (1, 'Основной'),
        (2, 'Дополнительный'),
    )

    type = models.SmallIntegerField(choices=TYPE, default=1, db_index=True, verbose_name='Тип', help_text='Тип контакта')
    phone = PhoneNumberField(verbose_name='ТелеФон')

    member = models.ForeignKey('Member', verbose_name='Участник', on_delete=models.PROTECT)

    def __str__(self):
        return '%s' % (self.phone)

class Ses(models.Model):
    class Meta:
        verbose_name = 'Сессия'
        verbose_name_plural = 'Сессии'

    MODE = (
        (0, 'Сброс'),
        (1, 'Активна'),
        (2, 'Заверщена'),
        (3, 'Выполнена'),
    )
    TYPE = (
        (0, 'Неизвестно'),
        (1, 'Заявка'),
        (2, 'Консултация'),
    )

    # type = models.SmallIntegerField(choices=TYPE, default=1, db_index=True, verbose_name='Тип', help_text='Тип сессии')
    mode = models.SmallIntegerField(choices=MODE, default=1, db_index=True, verbose_name='Режим', help_text='Режим сессии')
    ses_start = models.DateTimeField(default=timezone.now, null=True, blank=True, verbose_name='Начало')
    ses_stop = models.DateTimeField(null=True, blank=True, verbose_name='Окончание')

    member = models.ForeignKey('Member', verbose_name='Участник', on_delete=models.PROTECT)

    def __str__(self):
        return '%s - %s' % (self.mode, self.member)




