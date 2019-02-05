from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.

from .models import Distr, Code, ExceptCode
from catalog.models import Category, Vendor, Product

from catalog.models import Product

class CodeProdForm(forms.Form):

    title = forms.CharField(initial='Категория Вендор Артикул', help_text='Заголовок', label='Звголовок')
    iarticle = forms.CharField(required=False, label='Тех. артикул', help_text="Тех. артикул")
    article = forms.CharField(required=False, label='Артикул', help_text="Артикул")
    name = forms.CharField(required=False, widget=forms.Textarea)
    description = forms.CharField(required=False, widget=forms.Textarea)
    comment = forms.CharField(required=False, widget=forms.Textarea)
    url = forms.URLField(required=False, label='Ссылка')

    code = forms.CharField(required=False, label='Код дистрибьютора')

    cat = Category.objects.filter(type=1)
    vend = Vendor.objects.filter(type=1)
    distr = Distr.objects.filter(type=1)

    category = forms.ModelChoiceField(queryset=cat, initial=10)
    vendor = forms.ModelChoiceField(queryset=vend, initial=10)
    distr = forms.ModelChoiceField(queryset=distr)

    def save(self):
        title = self.cleaned_data['title']
        iarticle = self.cleaned_data['iarticle']
        article = self.cleaned_data['article']
        name = self.cleaned_data['name']
        description = self.cleaned_data['description']
        comment = self.cleaned_data['comment']
        url = self.cleaned_data['url']
        code = self.cleaned_data['code']
        cat = self.cleaned_data['category']
        vend = self.cleaned_data['vendor']
        distr = self.cleaned_data['distr']
        number = Product.set_number(self)
        #print(number)
        prod = Product(type=1, number=number, iarticle=iarticle, article=article, title=title, name=name, alias='',
                       description=description, comment=comment, url=url, img='', category=cat, vendor=vend)
        prod.save()
        if code:
            dc = Code(type=0, code=code, distr=distr, product_id=prod.id)
            dc.save()

        return "Товар "+title+" добавлен!"

class CodeJoinForm(forms.Form):
    code = forms.CharField(label='Код дистрибьютора')
    product = forms.IntegerField(required=False, label='ID продукта')
    description = forms.CharField(required=False, widget=forms.Textarea, label='Описание')


    distrs = Distr.objects.filter(type=1)
    distr = forms.ModelChoiceField(queryset=distrs)

    def clean_product(self):
        prod_id = self.cleaned_data['product']
        if prod_id:
            prod = Product.objects.filter(pk=prod_id)
            if not prod:
                raise ValidationError(_('Продукт с ID ' + str(prod_id) + ' отсутсьвует!'))

        # Помните, что всегда надо возвращать "очищенные" данные.
        return prod_id

    def save(self):
        code = self.cleaned_data['code']
        product = self.cleaned_data['product']
        distr = self.cleaned_data['distr']
        description = self.cleaned_data['description']

        result = ''
        if product:
            prod = Product.objects.filter(pk=product)
            if prod:
                prod = prod.first()
                dc = Code(type=0, code=code, distr=distr, product_id=prod.id)
                dc.save()
                result = 'Код ' + code + ' успешно добавлен к ' + prod.title
            else:
                result = 'Продукт с ID ' + product + ' отсутсьвует'

        else:
            exc = ExceptCode(type=1, code=code, description=description, comment='', distr=distr)
            exc.save()
            result = 'Код ' + code + ' успешно исключён!'

        return result






