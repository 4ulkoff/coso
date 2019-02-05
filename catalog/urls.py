from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='catindex'),
    path('search/', views.search, name='search'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product'),


]
