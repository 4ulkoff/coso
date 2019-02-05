from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='indexpars'),
    path('distr/<int:pk>/', views.distr_detail, name='distr'),
    path('uncode/<int:pk>/', views.uncode, name='uncode'),
    path('uncodelist/<int:pk>/', views.uncode_list, name='uncodelist'),
    path('uncodestep/<int:pk>/', views.uncode_step, name='uncodestep'),

]
