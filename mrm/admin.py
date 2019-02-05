from django.contrib import admin
from .models import Member, Phone, Email

# ================

class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 1
    max_num = 1

class EmailInline(admin.TabularInline):
    model = Email
    extra = 1
    max_num = 1

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'surname', 'name', 'patronymic', 'sex', 'phone', 'registration', 'id')
    list_filter = ('type', 'sex', )
    search_fields = ['title', 'surname', 'name', 'patronymic', 'email__email', 'phone__phone', ]

    fields = [('sex', 'type'), ('title', 'surname', 'name', 'patronymic'), 'registration']
    inlines = [PhoneInline, EmailInline]

    def phone(self, obj):
        p = None
        phone = Phone.objects.filter(type=1, member=obj)
        if phone:
            p = phone.first()

        return p











