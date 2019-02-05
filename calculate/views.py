from django.shortcuts import render

from catalog.models import Product
from .models import ActivSet

from .forms import ActivFormSet

# Create your views here.



def set(request):
    prod = request.GET.get('product', False)
    product = Product.objects.get(pk=prod)

    sign = 'добавлен'
    already = ActivSet.objects.filter(product_id=prod)
    if already:
        sign = 'уже добавлен'
    else:
        cnt = ActivSet.objects.filter(user=request.user).count()
        ins = ActivSet(user=request.user, product=product, value=1, order=cnt+1)
        ins.save()

    set = ActivSet.objects.filter(user=request.user).order_by('order')

    context = {
        'product': product,
        'set': set,
        'sign': sign,
    }
    return render(request, 'calculate/setlist.html', context)


def my_set(request):
    dset = request.GET.get('sdel', False)
    if dset:
        if dset == 'all':
            ActivSet.objects.filter(user=request.user).delete()
        else:
            sdel = ActivSet.objects.get(pk=dset)
            sdel.delete()


    set = ActivSet.objects.filter(user=request.user)

    context = {
        'product': '',
        'set': set,
        'sign': dset,
    }
    return render(request, 'calculate/myset.html', context)

from django.forms import modelformset_factory
from django import forms



def sets_add(request):

    dset = request.GET.get('sdel', False)
    if dset:
        if dset == 'all':
            ActivSet.objects.filter(user=request.user).delete()
        else:
            sdel = ActivSet.objects.get(pk=dset)
            sdel.delete()


    set = ActivSet.objects.filter(user=request.user)

#    ActivFormset = modelformset_factory(ActivSet, fields=('order', 'product', 'value',),
#                                        widgets={'product': forms.HiddenInput})
#                                        #TextInput(attrs={'class':'disabled', 'readonly':'readonly'})})    #forms.Textarea})
#    formset = ActivFormset(queryset=ActivSet.objects.filter(user=request.user).select_related())

    activ = ActivSet.objects.filter(user=request.user).select_related()
    data = []
    for a in activ:
        data.append({
            'order': a.order,
            'title': a.product.title,
            'volume': a.value,
            'product': a.product,
        })

    formset = ActivFormSet(initial=data)

    context = {
        'product': '',
        'set': set,
        'formset': formset,
        'sign': dset,
    }
    return render(request, 'calculate/sets.html', context)


from django.http import HttpResponseRedirect
from django.views.generic import CreateView

from .forms import SetForm, SetFormSet
from .models import Set


class SetCreateView(CreateView):
    template_name = 'calculate/formset.html'
    model = Set
    form_class = SetForm
    success_url = 'success/'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ingredient_form = SetFormSet()
        instruction_form = SetFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ingredient_form=ingredient_form,
                                  instruction_form=instruction_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ingredient_form = SetFormSet(self.request.POST)
        instruction_form = SetFormSet(self.request.POST)
        if (form.is_valid() and ingredient_form.is_valid() and
            instruction_form.is_valid()):
            return self.form_valid(form, ingredient_form, instruction_form)
        else:
            return self.form_invalid(form, ingredient_form, instruction_form)

    def form_valid(self, form, ingredient_form, instruction_form):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        self.object = form.save()
        ingredient_form.instance = self.object
        ingredient_form.save()
        instruction_form.instance = self.object
        instruction_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, ingredient_form, instruction_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  ingredient_form=ingredient_form,
                                  instruction_form=instruction_form))

