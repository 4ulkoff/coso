from django import forms
from django.forms.formsets import formset_factory


from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import Set, SetList


class SetForm(ModelForm):
    class Meta:
        model = Set
        fields = ('title', )


SetFormSet = inlineformset_factory(Set, SetList, fields=('product', ))

class SetsProductForm(forms.Form):
    order = forms.IntegerField()
    title = forms.CharField()
    volume = forms.IntegerField()
    product = forms.HiddenInput()

ActivFormSet = formset_factory(SetsProductForm)


