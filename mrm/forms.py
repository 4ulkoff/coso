from django import forms
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.

from parsing.models import Distr, Code, ExceptCode
from catalog.models import Category, Vendor, Product

from django.forms import inlineformset_factory

from .models import Member








class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ()

# MemberFormSet = inlineformset_factory(Phone, Member, form=MemberForm, extra=1)









