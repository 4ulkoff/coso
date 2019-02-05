from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.

from parsing.models import Distr, Code, ExceptCode
from catalog.models import Category, Vendor, Product




class SearchForm(forms.Form):
    ORDERS = [[1, 'От наименьшей'], [2, 'От наибольшей']]
    CHECKBOX = ((1, 'В наличие'), )

    q = forms.CharField(required=False, label='Поисковый запрос',
                        widget=forms.TextInput(attrs={'placeholder': 'Поисковый запрос', 'size': '50'}))
    number = forms.CharField(required=False, label='Код товара',
                        widget=forms.TextInput(attrs={'placeholder': 'Код товара', 'size': '50'}))

    available = forms.BooleanField(required=False, label='В наличии', initial=True)

    order = forms.ChoiceField(widget=RadioSelect(), label='По цене', choices=ORDERS, initial=1)

    cat = Category.objects.filter(type=1).order_by('name')
    vend = Vendor.objects.filter(type=1).order_by('vendor')
    distr = Distr.objects.filter(type=1)

    category = forms.ModelChoiceField(label='Категория',required=False, queryset=cat)
    vendor = forms.ModelChoiceField(label='Производитель',required=False, queryset=vend)
    distr = forms.ModelChoiceField(label='Дистрибьютор',required=False, queryset=distr)









