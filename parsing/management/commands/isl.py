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

from datetime import datetime, timedelta
from django.utils import timezone

from parsing.parsing import Parsing

from parsing.models import Forex, Matrix
import csv
import timeit


class Command(BaseCommand):
    help = 'Matrix'

    def handle(self, *args, **options):


        print('Вася!!!')
        a = timeit.default_timer()

        mx = Matrix.objects.filter(pk__gt=0, pk__lt=100000)
        print(len(mx))

        mp = 0
        mt = 0
        for mx in mx:
            mp += mx.point
            mt += mx.time
            print(mx.point, mx.time)
        print(mp, mt)
        print(timeit.default_timer() - a)

        """
        fx = Forex.objects.all()    # filter(pk__gt=0, pk__lt=1000)

        fst = Forex.objects.get(pk=1)
        bid = fst.bid
        tm = fst.time

        pnt = 0
        a = 0
        tt = timedelta(minutes=0)

        for f in fx:


            b = bid

            p = round((bid - f.bid)*100000, 0)

            p = int(p)
            bid = f.bid
            sec = f.time - tm
            tm = f.time

            if p > 0:

                if a == 0:

                    a = 1
                    print("V", pnt, int(tt.microseconds*0.001))
                    ins = Matrix(point=pnt, time=int(tt.microseconds*0.001))
                    ins.save()
                    pnt = 0
                    tt = timedelta(microseconds=0, seconds=0)

                pnt = pnt + p
                tt = sec + tt

                #print(type(sec))

            else:

                if a == 1:
                    a = 0
                    print("A", pnt, int(tt.microseconds*0.001))
                    ins = Matrix(point=pnt, time=int(tt.microseconds * 0.001))
                    ins.save()

                    pnt = 0
                    tt = timedelta(microseconds=0, seconds=0)
                pnt =  p + pnt
                tt = sec + tt



            #print(b, f.bid, p, sec)

        print(timeit.default_timer() - a)
        
        #

        f = DistrFile.objects.get(pk=122)

        dir = settings.MEDIA_ROOT+'/'
        file = dir+str(f.file)
        print(file)
        
        
        
        def csv_dict_reader(file_obj):
            a = timeit.default_timer()
            
            Read a CSV file using csv.DictReader
            

            reader = csv.DictReader(file_obj, delimiter=';')


            for line in reader:
                ask = float(line["Ask"].replace(',', '.'))
                bid = float(line["Bid"].replace(',', '.'))
                tm = datetime.strptime(line["Time (MSK)"], '%Y.%m.%d %H:%M:%S.%f').astimezone()
                # print(tm)

                fx = Forex(time=tm, ask=ask, bid=bid)
                fx.save()

                #print(line["Time (MSK)"], line["Ask"], line["Bid"])

            print(timeit.default_timer() - a)

        with open(file) as f_obj:
            csv_dict_reader(f_obj)
        """

#241.045
#1570.643
#179.145
#36.327
#726.216
#52.176
















