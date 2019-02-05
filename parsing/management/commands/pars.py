from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.cache import cache

import random

from parsing.parsing import Parsing, Victory
from parsing.models import DistrFile, Currency, DistrCurrency
from decimal import *


import os

from catalog.models import Product

# import urllib
from urllib import request
import xmltodict

from datetime import datetime
import xlrd
import openpyxl




def get_currency(date):
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    file = request.urlopen('https://nationalbank.kz/rss/get_rates.cfm?fdate=' + date)
    data = file.read()
    file.close()
    data = xmltodict.parse(data)
    i1 = list(data.items())
    i2 = list(i1[0][1].items())
    # i3 = list(i2[6][1].items())
    for e in i2[6][1]:
        i3 = list(e.items())
        if i3[1][1] == 'USD':
            rate = (i3[2][1])
            break
    return rate

def currency_analyser(distr_id):
    dcur = DistrCurrency.objects.filter(distr_id=distr_id)
    c_0 = 0
    c_1 = 0
    c_2 = 0
    c_3 = 0
    c1 = 0
    c2 = 0
    c3 = 0
    for dc in dcur:
        currency = Currency.objects.filter(date=dc.date)
        if currency:
            c = currency.first()
            per = (dc.rate - c.rate) / c.rate
            per = round(per * 100, 3)
            new_cur = c.rate * Decimal(1.005)
            new_cur = round(new_cur, 0)
            raz = dc.rate - new_cur
            if raz == 0.00:
                c_0 += 1
            if raz == 1.00:
                c_1 += 1
            if raz == 2.00:
                c_2 += 1
            if raz > 2.00:
                c_3 += 1
            if raz == -1.00:
                c1 += 1
            if raz == -2.00:
                c2 += 1
            if raz < -2.00:
                c3 += 1

        print(dc.date, c.rate, dc.rate, new_cur, dc.rate - new_cur, per, dc.distr)
    print(c_0, '|| +', c_1, c_2, c_3, '-', c1, c2, c3)

class Command(BaseCommand):
    help = 'Тестируем парсинг'

    def handle(self, *args, **options):
        pars = Parsing()
        f = DistrFile.objects.get(pk=60)
        pars.process(f)

        # cache.clear()
        # self.stdout.write('Cleared cache\n')

        # currency_analyser(13)

        # cur = get_currency('22.11.2018')
        # cc = float(cur) * 1.005
        # print(cc)
        # c = Currency.objects.get(date='2018-11-19')
        # print(cur, c.rate)

        # pars.get_uncode(f)
        # a = pars.process(f)
        # print(a)

        """
        file = DistrFile.objects.get(pk=49)
        lst = pars.exl_list(file.file)
        for l in lst:
            #cur = Currency(symbol=1, rate=l[2], date=l[0])
            #cur.save()

            date = datetime.strptime(l[5][0:10], '%Y-%m-%d').date()

            print(date, l[2], l[4])
            # cur = DistrCurrency(symbol=1, rate=l[4], date=date, distr_id=l[2])
            # cur.save()
        """

        # p = Product()
        # print(p.set_number())
