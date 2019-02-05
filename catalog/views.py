from django.shortcuts import render, redirect
from django.views import generic
from django.db.models import Q

from decimal import Decimal

from .forms import SearchForm

from .models import Category, Vendor, Product
from parsing.models import Price, Code, Stock

from _datetime import datetime

# ============================

def search_free(s1):
    found = [None] * 6
    if s1:
        found[0] = Product.objects.filter(article__icontains=s1)
        found[1] = Product.objects.filter(iarticle__icontains=s1)
        found[2] = Product.objects.filter(title__icontains=s1)
        found[3] = Product.objects.filter(name__icontains=s1)
        found[4] = Product.objects.filter(description__icontains=s1)
        found[5] = Product.objects.filter(alias__icontains=s1)

    fnd = list()
    for i in range(6):
        if found[i]:
            for f in found[i]:
                if f not in fnd:
                    fnd.append(f)
    return fnd

def search_depend(s1, cat, vend):
    found = [None] * 6
    found[0] = Product.objects.filter(article__icontains=s1)
    found[1] = Product.objects.filter(iarticle__icontains=s1)
    found[2] = Product.objects.filter(title__icontains=s1)
    found[3] = Product.objects.filter(name__icontains=s1)
    found[4] = Product.objects.filter(description__icontains=s1)
    found[5] = Product.objects.filter(alias__icontains=s1)
    if cat:
        found[0] = found[0].filter(category_id=cat)
        found[1] = found[1].filter(category_id=cat)
        found[2] = found[2].filter(category_id=cat)
        found[3] = found[3].filter(category_id=cat)
        found[4] = found[4].filter(category_id=cat)
        found[5] = found[5].filter(category_id=cat)
    if vend:
        found[0] = found[0].filter(vendor_id=vend)
        found[1] = found[1].filter(vendor_id=vend)
        found[2] = found[2].filter(vendor_id=vend)
        found[3] = found[3].filter(vendor_id=vend)
        found[4] = found[4].filter(vendor_id=vend)
        found[5] = found[5].filter(vendor_id=vend)



    fnd = list()
    for i in range(6):
        if found[i]:
            for f in found[i]:
                if f not in fnd:
                    fnd.append(f)
    return fnd

def index (request):
    cd = 1 # Product.objects.select_related(‘category’).get(pk=book_id)

    context = {
        'a': cd,
    }
    return render(request, 'catalog/index.html', context)

def marzha(price):
    price = float(price)
    if price < 1000:
        my=round(price * 1.09, -1)
    if price >= 1000:
        my = round(price * 1.08, -2)
    if price >= 5000:
        my = round(price * 1.07, -2)
    if price >= 10000:
        my = round(price * 1.06, -2)
    if price >= 30000:
        my = round(price * 1.05, -2)
    if price >= 50000:
        my = round(price * 1.04, -2)
    if price >= 100000:
        my = round(price * 1.04, -3)
    if price >= 150000:
        my = round(price * 1.04, -3)
    if price >= 200000:
        my = round(price * 1.03, -3)
    if price >= 300000:
        my = round(price * 1.03, -3)
    if price >= 400000:
        my = round(price * 1.03, -3)
    if price >= 500000:
        my = round(price * 1.03, -3)
    d = Decimal("1.00")
    my = Decimal(my) * d
    return my


import locale

def search (request):
    form = SearchForm(request.GET or None)
    result = list()
    coount_result = 0

    if request.GET:
        r = Price.objects.filter(type=1)
        #if request.GET.get('number', False):
        #    r = r.filter(product__number=request.GET['number'])
        if request.GET.get('q', False):
            q = request.GET.get('q', False)
            r = r.filter(Q(product__article__icontains=q) | Q(product__iarticle__icontains=q) |
                          Q(product__title__icontains=q) | Q(product__name__icontains=q) |
                          Q(product__description__icontains=q))
        if request.GET.get('category', False):
            r = r.filter(product__category_id=request.GET['category'])
        if request.GET.get('vendor', False):
            r = r.filter(product__vendor_id=request.GET['vendor'])
        if request.GET.get('distr', False):
            r = r.filter(code__distr_id=request.GET['distr'])
        if request.GET.get('available', False):
            r = r.filter(code__type=1)
        if request.GET['order']=='1':
            r = r.order_by('price')
        if request.GET['order']=='2':
            r = r.order_by('-price')

        for i in r:
            if i.price == 0:
                i.cp = 'Звоните'
                i.profit = 0
                i.percent = 0
            else:
                i.cp = marzha(i.price)
                i.profit = i.cp - i.price
                i.percent = round(((i.cp - i.price)/i.price)*100, 2)
                i.cp = '{0:,}'.format(i.cp).replace(',', ' ') + ' ₸'


            # print(i.cp)
            i.date = i.date.date()
            delta = datetime.today().date() - i.date
            ds = delta.days
            if ds > 21:
                i.cpcolor = 'warn'
                i.datecolor = 'warn'
            elif ds < 8:
                i.cpcolor = 'ok'
                i.datecolor = 'ok'

            if i.code.type == 1:
                i.available = 'В наличии'
                i.avcolor = 'ok'

                stc = Stock.objects.filter(type=1, code_id=i.code_id)
                if stc:
                    stc = stc.first()
                    sv = str(stc.value)
                    svar = ''
                    if stc.var == 1:
                        svar = '>'
                    if stc.var == 2:
                        svar = '<'

                    i.available = i.available + " (" + svar + sv + ")"
            else:
                i.available = 'На заказ'

           # print(i.stock)
            result.append(i)

        coount_result = len(r)


    context = {
        'form': form,
        'result': result,
        'coount_result': coount_result,

    }

    return render(request, 'catalog/search.html', context)




"""
def search (request):
    fsrch = list()
    fscount = 0
    dsrch = list()
    dscount = 0
    sprod = list()
    sprc = 0
    if request.method == 'POST':
        if request.POST['free']:
            fsrch = search_free(request.POST['free'])
            fscount = len(fsrch)
        if request.POST['depend']:
            dsrch = search_depend(request.POST['depend'], request.POST['category'], request.POST['vendor'])
            dscount = len(dsrch)


        if request.POST['category'] or request.POST['vendor']:
            if not request.POST['vendor']:
                sprod = Product.objects.filter(category_id=request.POST['category'])
            if not request.POST['category']:
                sprod = Product.objects.filter(vendor_id=request.POST['vendor'])
            if request.POST['category'] and request.POST['vendor']:
                sprod = Product.objects.filter(category_id=request.POST['category'], vendor_id=request.POST['vendor'])
            sprc = len(sprod)


    cats = Category.objects.filter(type=1)
    vendors = Vendor.objects.filter(type=1)

    context = {
        'cats': cats,
        'vendors': vendors,
        'fsrch': fsrch,
        'fscount': fscount,
        'dsrch': dsrch,
        'dscount': dscount,
        'sprod': sprod,
        'sprc': sprc,
    }
    return render(request, 'catalog/search.html', context)
"""

class ProductDetailView(generic.DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['price_list'] = Price.objects.filter(product_id=self.kwargs.get('pk')).order_by('-date')
        context['distr_list'] = Code.objects.filter(product_id=self.kwargs.get('pk'), type=1)

        return context



