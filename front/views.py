from django.shortcuts import render, redirect
from django.db.models import Q

from decimal import Decimal

from catalog.models import Product, Vendor, Category

from parsing.models import Code, Price
from .forms import VisitorSearchForm
from catalog.forms import SearchForm

# Create your views here.

def catalog_front(request):
    value = 'Hi!!!'



    vendors = Vendor.objects.filter(type=1)
    cats = Category.objects.filter(type=1)
    cprod = Product.objects.count()
    cpc = Product.objects.filter(category_id=50).count()
    cnout = Product.objects.filter(category_id=30).count()
    cmon = Product.objects.filter(category_id=31).count()
    smart = Product.objects.filter(category_id=58).count()
    tabs = Product.objects.filter(category_id=70).count()

    ccpu = Product.objects.filter(category_id=11).count()
    cmb = Product.objects.filter(category_id=12).count()
    cvc = Product.objects.filter(category_id=14).count()
    cram = Product.objects.filter(category_id=13).count()
    cssd = Product.objects.filter(category_id=16).count()
    chdd = Product.objects.filter(category_id=15).count()
    cbp = Product.objects.filter(category_id=17).count()
    ccase = Product.objects.filter(category_id=18).count()
    ccasebp = Product.objects.filter(category_id=19).count()
    coptic = Product.objects.filter(category_id=22).count()
    ccool = Product.objects.filter(category_id=20).count()
    cwater = Product.objects.filter(category_id=200).count()
    ccompl = ccpu+cmb+cvc+cram+cssd+chdd+cbp+ccase+ccasebp+coptic+ccool+cwater

    form = VisitorSearchForm(request.GET or None)
    result = list()
    coount_result = 0
    category = ''
    vendor = ''
    q = ''

    if request.GET:
        r = Code.objects.select_related()
        if request.GET['q']:
            q = request.GET['q']
            r = r.filter(Q(product__article__icontains=q) | Q(product__iarticle__icontains=q) |
                         Q(product__title__icontains=q) | Q(product__name__icontains=q) |
                         Q(product__description__icontains=q))
        if request.GET['category']:
            category = request.GET['category']
            r = r.filter(product__category_id=request.GET['category'])
        if request.GET['vendor']:
            vendor = request.GET['vendor']
            r = r.filter(product__vendor_id=request.GET['vendor'])

        result = r.order_by('product__nubber')
        coount_result = len(r)

    context = {
        'form': form,
        'result': result,
        'coount_result': coount_result,
        'q': q,
        'category': category,
        'vendor': vendor,
        'vendor_list': vendors,
        'cat_list': cats,
        'cprod': cprod,
        'ccat': len(cats),
        'cpc': cpc,
        'cnout': cnout,
        'cmon': cmon,
        'cvend': len(vendors),
        'ccompl': ccompl,
        'smart': smart,
        'tabs': tabs,
        'ccpu': ccpu,
        'cmb': cmb,
        'cvc': cvc,
        'cram': cram,
        'cssd': cssd,
        'chdd': chdd,
        'cbp': cbp,
        'ccase': ccase,
        'ccasebp': ccasebp,
        'coptic': coptic,
        'ccool': ccool,
        'cwater': cwater,
        'value': value,
    }

    return render(request, 'front/catalog-all.html', context)

def count_vendor(dct, cat=False):
    for i in dct:
        q = Product.objects.filter(vendor_id=dct[i])
        if cat:
            q = q.filter(category_id=cat)
        dct[i] = q.count()
    return dct

def count_category(dct, vend=False):
    for i in dct:
        q = Product.objects.filter(category_id=dct[i])
        if vend:
            q = q.filter(vendor_id=vend)
        dct[i] = q.count()
    return dct


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

def opt_pc(request):
    form = SearchForm(initial={'category': 50})
    pc_count = Product.objects.filter(category_id=50).count()
    vnd_lst = {'dell': 76, 'hp': 14, 'acer': 49, 'lenovo': 46}
    cat_lst = {'cpu': 11, 'mb': 12, 'ram':13, 'graph': 14, 'hdd': 15, 'ssd': 16, 'power': 17, 'case': 18}
    cntv = count_vendor(vnd_lst, 50)
    cntc = count_category(cat_lst)
    components = 0
    for i in cntc:
        components += cntc[i]

    r = Price.objects.filter(type=1, price__gt=0).filter(product__category_id=50).order_by('price')[0:20]
    tab = list()
    for i in r:
        i.price = marzha(i.price)
        i.price = '{0:,}'.format(i.price).replace(',', '\xa0') + '\xa0₸'
        tab.append(i)

    context = {
        'form': form,
        'tab': tab,
        'pc_count': pc_count,
        'cntv': cntv,
        'cntc': cntc,
        'components': components,
    }
    return render(request, 'front/opt_pc.html', context)

def opt_nout(request):
    form = SearchForm(initial={'category': 30})
    all_count = Product.objects.filter(category_id=30).count()
    vnd_lst = {'dell': 76, 'hp': 14, 'acer': 49, 'lenovo': 46, 'apple': 98, 'msi': 71, 'asus': 17, 'dream': 250}
    cat_lst = {'battery': 93, 'vr': 99, 'extcd': 223, 'exthdd': 21, 'sd': 89, 'cartreader': 117, 'webcam': 86,
               'akust': 97, 'keyboard': 25, 'keymouse': 26, 'kovrik': 127, 'mfu': 28, 'mouse': 24, 'naush': 56,
               'akustportable': 74, 'printer': 29, 'software': 54, 'scaner': 80, 'sumkanout': 75, 'flesh': 45}

    cntv = count_vendor(vnd_lst, 30)
    cntc = count_category(cat_lst)
    components = 0

    for i in cntc:
        components += cntc[i]

    nts = Price.objects.filter(type=1, price__gt=0).filter(product__category_id=30).order_by('price')[0:20]
    nouts = list()
    for i in nts:
        i.price = marzha(i.price)
        i.price = '{0:,}'.format(i.price).replace(',', '\xa0') + '\xa0₸'
        nouts.append(i)

    # print(nouts)

    context = {
        'form': form,
        'nouts': nouts,
        'all_count': all_count,
        'cntv': cntv,
        'cntc': cntc,
        'components': components,
    }
    return render(request, 'front/opt_nout.html', context)

def opt_monoblock(request):
    form = SearchForm(initial={'category': 31})
    all_count = Product.objects.filter(category_id=31).count()
    vnd_lst = {'dell': 76, 'hp': 14, 'acer': 49, 'lenovo': 46, 'apple': 98, 'msi': 71, 'asus': 17, 'dream': 250}
    cat_lst = {'battery': 93, 'vr': 99, 'extcd': 223, 'exthdd': 21, 'sd': 89, 'cartreader': 117, 'webcam': 86,
               'akust': 97, 'keyboard': 25, 'keymouse': 26, 'kovrik': 127, 'mfu': 28, 'mouse': 24, 'naush': 56,
               'akustportable': 74, 'printer': 29, 'software': 54, 'scaner': 80, 'sumkanout': 75, 'flesh': 45}

    cntv = count_vendor(vnd_lst, 31)
    cntc = count_category(cat_lst)
    components = 0

    for i in cntc:
        components += cntc[i]

    nts = Price.objects.filter(type=1, price__gt=0).filter(product__category_id=31).order_by('price')[0:20]
    nouts = list()
    for i in nts:
        i.price = marzha(i.price)
        i.price = '{0:,}'.format(i.price).replace(',', '\xa0') + '\xa0₸'
        nouts.append(i)

    # print(nouts)

    context = {
        'form': form,
        'nouts': nouts,
        'all_count': all_count,
        'cntv': cntv,
        'cntc': cntc,
        'components': components,
    }
    return render(request, 'front/opt_monoblock.html', context)

def bootstrap(request):
    return render(request, 'front/bootstrap.html', {})

def isti(request):
    return render(request, 'front/isti.html', {})




