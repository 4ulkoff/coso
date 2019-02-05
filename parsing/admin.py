from django.contrib import admin
from .models import Distr, Code, ExceptCode, DistrFile, DistrCategory, Price, DistrCurrency
from catalog.models import Product

# Register your models here.

@admin.register(Distr)
class DistrAdmin(admin.ModelAdmin):
    list_display = ('distr', 'id', 'alias')


@admin.register(Code)
class CodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'id', 'distr', 'product', 'type')
    list_filter = ('distr', 'type',)
    search_fields = ['code', ]


@admin.register(ExceptCode)
class ExceptCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'distr', 'description', 'id')
    list_filter = ('distr', 'type',)
    search_fields = ['code', ]

@admin.register(DistrCategory)
class DistrCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'type', 'distr', 'id')
    list_filter = ('distr', 'type', )

@admin.register(DistrFile)
class DistrFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'distr', 'date', 'count', 'count_new', 'type')
    list_filter = ('distr', )


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'date', 'distr', 'type', 'id')
    list_filter = ('distr', 'type', )
    search_fields = ['product', ]
    readonly_fields = ['product', 'code',]


@admin.register(DistrCurrency)
class DistrCurrencyAdmin(admin.ModelAdmin):
    list_display = ('date', 'rate', 'symbol', 'distr', 'id')
    list_filter = ('distr', 'symbol', )
    search_fields = ['rate', 'dare', ]




