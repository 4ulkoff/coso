from django.urls import path
from . import views

urlpatterns = [
    path('sets/', views.set, name='set'),
    path('myset/', views.my_set, name='myset'),
    path('addset/', views.sets_add, name='setadd'),
    path('set/', views.SetCreateView.as_view(), name='create'),

]
