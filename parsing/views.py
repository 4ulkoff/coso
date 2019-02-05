from django.shortcuts import render, redirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from datetime import datetime

from django.conf import settings
from django.core.files import File
import openpyxl
import re

from .parsing import Parsing

from .models import Distr, DistrFile, DistrCategory, ExceptCode
from catalog.models import Category, Vendor, Product

from .forms import CodeProdForm, CodeJoinForm

# =================================

def search_prod(iarticle, article, free=False):
    found = [None] * 15
    if article:
        found[0] = Product.objects.filter(article__icontains=article)
        found[1] = Product.objects.filter(iarticle__icontains=article)
        found[2] = Product.objects.filter(title__icontains=article)
        found[3] = Product.objects.filter(name__icontains=article)
        found[4] = Product.objects.filter(description__icontains=article)
    if iarticle:
        found[5] = Product.objects.filter(article__icontains=iarticle)
        found[6] = Product.objects.filter(iarticle__icontains=iarticle)
        found[7] = Product.objects.filter(title__icontains=iarticle)
        found[8] = Product.objects.filter(name__icontains=iarticle)
        found[9] = Product.objects.filter(description__icontains=iarticle)
    if free:
        found[10] = Product.objects.filter(article__icontains=free)
        found[11] = Product.objects.filter(iarticle__icontains=free)
        found[12] = Product.objects.filter(title__icontains=free)
        found[13] = Product.objects.filter(name__icontains=free)
        found[14] = Product.objects.filter(description__icontains=free)

    fnd = list()
    for i in range(15):
        if found[i]:
            for f in found[i]:
                if f not in fnd:
                    fnd.append(f)
    return fnd

"""
class MyView(PermissionRequiredMixin, View):
    # permission_required = 'catalog.can_mark_returned'
    # Or multiple permissions
    permission_required = ('catalog.can_mark_returned', 'catalog.can_edit')
    # Note that 'catalog.can_edit' is just an example
    # the catalog application doesn't have such permission!
"""

@permission_required('catalog.add_category')
def index(request):
    distr_list = Distr.objects.filter(type=1)
    context = {
        'head' : 'Дистрибьютор',
        'distr_list': distr_list,


    }

    return render(request, 'parsing/index.html', context)

def distr_pars(request, pk):
    distr_list = Distr.objects.filter(type=1)
    distr = Distr.objects.get(pk=pk)
    d = Distr.objects.get(pk=11)
    ca = Category.objects.get(pk=10)

    f = DistrFile.objects.get(pk=12)
    a = File(f.file)
    exl = exl_list(a)
    value = 0
    pars = list()
    cat = 10

    # Перебираем Excel
    for a in exl:
        # Если нет ID
        if a[0] == "None":
            # Дата
            if re.match(r'Создан:', a[2]):
                day = re.findall(r'\d{2}.\d{2}.\d{4}', a[2])[0]
                time = re.findall(r'\d{2}:\d{2}', a[2])[0]
                dt = day+time
                date = datetime.strptime(dt, '%d.%m.%Y%H:%M').strftime('%Y-%m-%d %H:%M:00+06:00')
            # Категория
            if a[1]:
                c = DistrCategory.objects.filter(distr=11, name=a[1])

                # Катешория в базе
                if c:
                    cf = c.first()
                    cat = cf.category
                # Добавляем категорию в базу
                else:
                    ins = DistrCategory(type=3, name=a[1], category_id=ca.pk, distr_id=d.pk)
                    ins.save()
        # Строки с товаром
        else:
            # Парсим вендора из описания
            v = Vendor.objects.filter(type=1)
            vendor_list = list()
            for vend in v:
                find = re.search(r'\b{}\b'.format(vend.vendor), a[2], re.IGNORECASE)
                if find:
                    vendor_list.append(vend.id)
            vendor = list()
            for i in vendor_list:
                vnd = Vendor.objects.get(pk=i)
                vendor.append(vnd)


            code = a[0].replace('ID:     ', 'ID:')
            exc = ExceptCode.objects.filter(distr_id=11, code=code)

            if not exc:
                article = a[1].replace(' oem', '')
                row_data = (code, a[3], '', '', 0, article, a[2], a[2], '', vendor, cat, "")
                pars.append(row_data)
                value += 1




    exl = pars
    f.date = date
    f.save()






    context = {
        'head' : 'Дистрибьютор',
        'distr_list': distr_list,
        'dpk': pk,
        'link': 'list',
        'name': distr.distr,
        'exl': exl,
        'value': value,

    }

    return render(request, 'parsing/distr.html', context)

def distr_detail(request, pk):
    distr_list = Distr.objects.filter(type=1)
    distr = Distr.objects.get(pk=pk)
    files = DistrFile.objects.filter(type=3, distr_id=pk)
    value = ""

    #d = Distr.objects.get(pk=11)

    context = {
        'head': 'Дистрибьютор',
        'distr_list': distr_list,
        'dpk': pk,
        'link': 'list',
        'name': distr.distr,
        'uncode': files,
        'value': value,

    }

    return render(request, 'parsing/distr_detail.html', context)

# Вывод списка товаров не в базе
def uncode_list(request, pk):
    form = CodeProdForm(request.POST or None)
    result = ''
    if request.method == 'POST' and form.is_valid():
        result = form.save()

    if request.method == 'GET':
        form = CodeJoinForm(request.GET or None)
        if form.is_valid():
            result = form.save()

    pars = Parsing()
    file = DistrFile.objects.get(pk=pk)
    distr_list = Distr.objects.filter(type=1)
    distr = Distr.objects.get(pk=file.distr_id)
    undc_list = pars.get_uncode(file)   # Список не добавленных кодов
    count = len(undc_list)
    udc = list()
    founds = list()
    # Подготовка контента
    for undc in undc_list:
        found = [None]*6
        if undc['article']:
            found[0] = Product.objects.filter(article__icontains=undc['article'])
            found[1] = Product.objects.filter(iarticle__icontains=undc['article'])
            found[2] = Product.objects.filter(name__icontains=undc['article'])

        if undc['iarticle']:
            found[3] = Product.objects.filter(article__icontains=undc['iarticle'])
            found[4] = Product.objects.filter(iarticle__icontains=undc['iarticle'])
            found[5] = Product.objects.filter(name__icontains=undc['iarticle'])

        fnd = list()
        for i in range(6):
            if found[i]:
                for f in found[i]:
                    if f not in fnd:
                        fnd.append(f)

        fnd_count = len(fnd)

        cat = undc['category']
        vend = undc['vendor'][0]  #[len(undc['vendor'])-1]

        products = Product.objects.filter(category_id=cat, vendor_id=vend)

        title = cat.name + ' ' +vend.vendor + ' ' + undc['article']

        all_cat = Category.objects.filter(type=1)
        vendors = Vendor.objects.filter(type=1)

        raw = {
            'source': undc,
            'title': title,
            'cats': all_cat,
            'vendors': vendors,
            'founds': fnd,
            'fnd_count': fnd_count,
            'products': products,
        }
        udc.append(raw)

    context = {
        'head': 'Дистрибьютор',
        'distr_list': distr_list,
        'distr': distr,
        'dpk': distr.pk,
        'form': form,
        'udc_list': udc,
        'uncode': file.file,
        'count': count,
        'result': result,
    }

    return render(request, 'parsing/uncode_list.html', context)

# Пошаговый вывод товаров не в базе
def uncode_step(request, pk):
    form = CodeProdForm()
    result = ''
    srch = None
    scode = None
    sprod = None
    search = False
    scount = 0
    ttl = None
    if request.method == 'POST':
        label = request.POST['label']
        if label == 'search':
            srch = search_prod(request.POST['article'], request.POST['iarticle'], request.POST['free'])
            scode = request.POST['code']
            scount = len(srch)

            sprod = Product.objects.filter(category_id=request.POST['category'], vendor_id=request.POST['vendor'])
            search = True
            if request.POST['article']:
                ct = Category.objects.get(pk=request.POST['category'])
                vn = Vendor.objects.get(pk=request.POST['vendor'])
                ttl = ct.name + ' ' + vn.vendor + ' ' + request.POST['article']

        if label == 'add':
            form = CodeProdForm(request.POST or None)
            if form.is_valid():
                result = form.save()

    if request.method == 'GET':
        form = CodeJoinForm(request.GET or None)
        if form.is_valid():
            result = form.save()

    pars = Parsing()
    file = DistrFile.objects.get(pk=pk)
    distr_list = Distr.objects.filter(type=1)
    distr = Distr.objects.get(pk=file.distr_id)
    undc_list = pars.get_uncode(file, step=True)    # Список не добавленных кодов (пошагово)
    if not undc_list:
        return redirect('distr', file.distr_id)
    undc = undc_list[0]
    cat = undc['category']
    vend = undc['vendor'][0]
    if not search:
        srch = search_prod(undc['article'], undc['iarticle'])
        scode = undc['code']
        scount = len(srch)
        sprod = Product.objects.filter(category_id=cat, vendor_id=vend)

    title = cat.name + ' ' + vend.vendor + ' ' + undc['article']
    if ttl:
        title = ttl
        undc['category'] = ct
        undc['vendor'][0] = vn
        undc['article'] = request.POST['article']
        if request.POST['iarticle']:
            undc['iarticle'] = request.POST['iarticle']
    # print(undc)

    all_cat = Category.objects.filter(type=1)
    vendors = Vendor.objects.filter(type=1)
    raw = {
        'source': undc,
        'title': title,
        'cats': all_cat,
        'vendors': vendors,
    }
    udc = list()
    udc.append(raw)
    """
    count = len(undc_list)
    udc = list()
    founds = list()
    # Подготовка контента
    for undc in undc_list:
        cat = undc['category']
        vend = undc['vendor'][0]  # [len(undc['vendor'])-1]
        # Автоматический поиск
        if not search:
            srch = search_prod(undc['article'], undc['iarticle'])
            scode = undc['code']
            scount = len(srch)
            sprod = Product.objects.filter(category_id=cat, vendor_id=vend)

        title = cat.name + ' ' + vend.vendor + ' ' + undc['article']
        if ttl:
            title = ttl
            cat = ct
            vend = vn

        all_cat = Category.objects.filter(type=1)
        vendors = Vendor.objects.filter(type=1)

        raw = {
            'source': undc,
            'title': title,
            'cats': all_cat,
            'vendors': vendors,
            }
        udc.append(raw)

    """
    context = {
        'head': 'Дистрибьютор',
        'distr_list': distr_list,
        'distr': distr,
        'dpk': distr.pk,
        'form': form,
        'udc_list': udc,
        'search': search,
        'srch': srch,
        'scode': scode,
        'scount': scount,
        'sprod': sprod,
        'result': result,
    }

    return render(request, 'parsing/uncode_step.html', context)

# Вывод товаров не в базе
def uncode(request, pk):
    form = CodeProdForm(request.POST or None)
    result = ''
    if request.method == 'POST' and form.is_valid():
        result = form.save()

    if request.method == 'GET':
        form = CodeJoinForm(request.GET or None)
        if form.is_valid():
            result = form.save()

    pars = Parsing()
    file = DistrFile.objects.get(pk=pk)
    distr_list = Distr.objects.filter(type=1)
    distr = Distr.objects.get(pk=file.distr_id)
    undc_list = pars.get_uncode(file)   # Список не добавленных кодов
    count = len(undc_list)
    udc = list()
    founds = list()
    # Подготовка контента
    for undc in undc_list:
        found = [None]*6
        if undc['article']:
            found[0] = Product.objects.filter(article__icontains=undc['article'])
            found[1] = Product.objects.filter(iarticle__icontains=undc['article'])
            found[2] = Product.objects.filter(name__icontains=undc['article'])

        if undc['iarticle']:
            found[3] = Product.objects.filter(article__icontains=undc['iarticle'])
            found[4] = Product.objects.filter(iarticle__icontains=undc['iarticle'])
            found[5] = Product.objects.filter(name__icontains=undc['iarticle'])

        fnd = list()
        for i in range(6):
            if found[i]:
                for f in found[i]:
                    if f not in fnd:
                        fnd.append(f)

        fnd_count = len(fnd)

        cat = undc['category']
        vend = undc['vendor'][0]  #[len(undc['vendor'])-1]

        products = Product.objects.filter(category_id=cat, vendor_id=vend)

        title = cat.name + ' ' +vend.vendor + ' ' + undc['article']

        all_cat = Category.objects.filter(type=1)
        vendors = Vendor.objects.filter(type=1)

        raw = {
            'source': undc,
            'title': title,
            'cats': all_cat,
            'vendors': vendors,
            'founds': fnd,
            'fnd_count': fnd_count,
            'products': products,
        }
        udc.append(raw)

    context = {
        'head': 'Дистрибьютор',
        'distr_list': distr_list,
        'distr': distr,
        'dpk': distr.pk,
        'form': form,
        'udc_list': udc,
        'uncode': file.file,
        'count': count,
        'result': result,
    }

    return render(request, 'parsing/uncode.html', context)


