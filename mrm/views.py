from django.shortcuts import render












from .forms import *
from django.forms.models import modelformset_factory
from django.forms.models import inlineformset_factory

from .models import *


# Create your views here.

def index(request):
    context = {}
    return render(request, 'mrm/ask_add.html', context)

def ask_add(request):
    form = MemberForm(request.POST or None)
    # MemberFormSet = modelformset_factory(Member)
    MyForm = inlineformset_factory(Member, Phone, exclude=['registration', ], extra=2)
    form = MyForm   # MemberFormSet()
    EmailForm = inlineformset_factory(Member, Email, exclude=['registration', ], extra=2)
    eform = EmailForm
    context = {
        'form': form,
        'eform': eform,
    }

    return render(request, 'mrm/ask_add.html', context)