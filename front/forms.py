from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.

from parsing.models import Distr, Code, ExceptCode
from catalog.models import Category, Vendor, Product



class VisitorSearchForm(forms.Form):


    q = forms.CharField(required=False, label='Поисковый запрос',
                        widget=forms.TextInput(attrs={'placeholder': 'Поиск', 'size': '20'}))

    cat = Category.objects.filter(type=1).order_by('name')
    vend = Vendor.objects.filter(type=1).order_by('vendor')


    category = forms.ModelChoiceField(label='Категория',required=False, queryset=cat)
    vendor = forms.ModelChoiceField(label='Производитель',required=False, queryset=vend)









