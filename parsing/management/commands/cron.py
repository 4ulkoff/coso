from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.files import File
from parsing.models import Distr, DistrFile
from django.core.files.storage import FileSystemStorage

import os
import random
import patoolib
import shutil
import re

from datetime import datetime
from django.utils import timezone

from parsing.parsing import Parsing

def remove_price(file):
    oldext = os.path.splitext(file)[1]
    newname = str(random.randint(100000000000, 999999999999))+oldext
    dir = settings.MEDIA_ROOT + '/price/'
    newfile = dir+newname
    if os.path.isfile(newfile):
        newname = str(random.randint(100000000000, 999999999999)) + oldext

    shutil.move(file, dir + newname)
    return 'price/' + newname

class Command(BaseCommand):
    help = 'Pars prices'

    def handle(self, *args, **options):



        distr = {
            11: 'victory/',
            12: 'redington/',
            13: 'vstrade/',
            14: 'marvel/',
            15: 'arenas/',
            16: 'moontech/',
            17: 'comportal/',
            18: 'alstyle/',
        }

        for i in distr:
            price = '/price_tmp/'+distr[i]
            dir = settings.MEDIA_ROOT + price
            files = os.listdir(dir)


            # Распаковываем и удаляем архивы
            if i == 16 or i ==  14:
                for f in files:
                    file = dir + f
                    patoolib.extract_archive(file, outdir=dir)
                    os.remove(file)
                files = os.listdir(dir)

            for f in files:
                tp = 2
                date = timezone.now()
                file = dir+f

                # Даты для Redingtona и VS Trade
                if i == 12 or i == 13:
                    day = re.findall(r'\d{2}.\d{2}.\d{4}', f)[0]
                    date = datetime.strptime(day + '00:00', '%d.%m.%Y%H:%M').astimezone()

                # Даты для Marvel
                if i == 14:
                    day = re.findall(r'\d{2}_\d{2}_\d{4}', f)[0]
                    date = datetime.strptime(day + '00:00', '%d_%m_%Y%H:%M').astimezone()

                # Дата и тип для ComPortala
                if i == 17:
                    if f[0:7] == 'Остатки':
                        d = f[8:10]
                        m = f[11:13]
                        date = datetime.strptime(d+'.'+m+'.2018' + '00:00', '%d.%m.%Y%H:%M').astimezone()
                    else:
                        date = datetime.strptime(f[0:10] + '00:00', '%d.%m.%Y%H:%M').astimezone()
                        tp = 1

                # Дата для Муна
                if i == 16:
                    date = datetime.strptime(f[10:18] + '00:00', '%d%m%Y%H:%M').astimezone()

                # Дата для Al-Style
                if i == 18:
                    date = datetime.strptime(f[-24:-5], '%Y-%m-%d_%H_%M_%S').astimezone()

                filename = remove_price(file=file)
                d = Distr.objects.get(pk=i)
                ins = DistrFile(type=tp, date=date, count=0, count_new=0, file=filename, distr=d)
                print(f, tp, date, distr[i])
                ins.save()





        p = Parsing()
        p.go()








