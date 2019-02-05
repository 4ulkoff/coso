from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from front import views










urlpatterns = [
    path('catalogs/', views.catalog_front, name='catalogs'),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('optom/', views.opt_pc, name='optom'),
    path('komputery_optom', views.opt_pc, name='opt_pc'),
    path('noutbuki-optom', views.opt_nout, name='opt_nout'),
    path('monobloki_optom', views.opt_monoblock, name='opt_monoblock'),
    path('bootstrap', views.bootstrap, name='bootstrap'),
    path('isti', views.isti, name='isti'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('parsing/', include('parsing.urls')),
    path('catalog/', include('catalog.urls')),
    path('mrm/', include('mrm.urls')),
    path('calculate/', include('calculate.urls')),
    path('admin/', admin.site.urls),
]

from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()



