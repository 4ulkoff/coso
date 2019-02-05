from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='indexmrm'),
    path('ask/add/', views.ask_add, name='ask_add'),


]
