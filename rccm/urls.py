from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    
     path('', views.index, name='rccm.dashboard'),
     path('formalite/modification/', views.modification, name='rccm.modification'),
     path('formalite/creation/', views.formalite, name='rccm.formalite'),
     path('formalite/creation-rapide/<pk>', views.formaliteRapide, name='rccm.formalite-rapide'),
     path('formalite/detail-formalite/<slug>', views.detail, name='rccm.formalite.detail'),
     path('form/search-rccm/', views.search_rccm, name='search_rccm'),
     path('form/save-formalite/', views.submit_formalite, name='rccm.submitFormalite'),
     path('form/update-formalite/<int:pk>/', views.update_formalite, name='formalite.update'),
     path('form/save-rccm/', views.submit_rccm, name='rccm.submitRccm'),
     path('form/rccms/', views.rccm, name='rccm.list'),
     path('form/rccm-detail/<pk>/', views.rccm_detail, name='rccm.detail'),
     path('rccm/creation', views.create_rccm, name='rccm.create'),
     path('scan/', views.scan, name='rccm.scan'),
     path('signature/<slug>', views.scanFormalite, name='formalite.scan'),
     path('signature-formalite/', views.signFormalite, name='formalite.sign'),
     path('suppression-formalite/', views.deleteFormalite, name='formalite.delete'),
     path('get-options/', views.get_options_by_declaration, name='get_options_by_declaration'),
     path('formalites/export-excel/', views.export_excel, name='export_excel'),


       
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)