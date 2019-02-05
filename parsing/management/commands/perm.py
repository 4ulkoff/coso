from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from django.contrib.auth.models import Permission
import random

from parsing.parsing import Parsing, Victory
from parsing.models import DistrFile

from catalog.models import Product


def get_user_permissions(user):
    if user.is_superuser:
        return Permission.objects.all()
    return user.user_permissions.all() | Permission.objects.filter(group__user=user)

class Command(BaseCommand):
    help = 'Тестируем парсинг'

    def handle(self, *args, **options):
        u = User.objects.get(username='Alan')
        per = Permission.objects.filter(group__user=u)
        for p in per:
            print(p.content_type.app_label, p.codename)



