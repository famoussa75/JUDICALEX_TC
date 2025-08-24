from django.urls import path, include
from . import views

urlpatterns = [
     path('', views.index, name='role.index'),
     path('roles/', views.listRole, name='role.liste'),
     path('roles/export/', views.export_roles_excel, name='role.export'),
     path('roles/valide/<int:pk>/', views.valide_role, name='role.valider'),
     path('affaires/', views.listAffaire, name='role.affaires'),
     path('affaires/details/<idAffaire>', views.detailAffaire, name='affaires.details'),
     path('affaires/export/', views.export_affaires_excel, name='affaires.export'),
     path('roles/update', views.updateRole, name='role.update'),
     path('roles/delete', views.deleteRole, name='role.delete'),
     path('decisions/delete', views.deleteDecision, name='decision.delete'),
     path('decisions/update/', views.update_decision, name='decision.update'),
     path('creation-role/', views.createRole, name='role.create'),
     path('enrollement/', views.listEnrollement, name='role.enrollement'),
     path('enrollement/list/', views.listEnrollementForAdmin, name='role.enrollementForAdmin'),
     path('affaires/<int:id>/cancel/', views.cancel_affaire, name='affaires.cancel'),
     path('affaires/edit/<idAffaire>', views.edit_affaire, name='affaires.edit'),
     path('admin/enrollements/<int:idJuridiction>/export/', views.export_enrollements_excel, name='export_enrollements_excel'),
     path('export/pdf/<int:juridiction_id>/', views.export_enrollements_pdf, name='export_enrollements_pdf'),
     path('historique/enrollement/<int:pk>/', views.historique_modifications_enrollement, name='historique_modifications_enrollement'),
     path('historique/decisions/<int:pk>/', views.historique_modifications_decisions, name='historique_modifications_decisions'),
     path('creation-enrollement/', views.createEnrollement, name='role.createEnrollement'),
     path('details/<pk>', views.roleDetail, name='role.detail'),
     path('gestion-messages/', views.ges_message, name='ges_message'),
     path('gestion-messages/<int:pk>/<str:action>/', views.ges_message, name='gestion_messages_edit'),

     path('fetch-form/<selectedJuridiction>/<selectedType>/<selectedSection>/<dateRole>/', views.fetchForm, name='role.fetchForm'),
     path('fetch-form-enrollement/<selectedJuridiction>/<selectedType>/', views.fetchFormEnrollement, name='role.fetchFormEnrollement'),

     path('download-pdf/', views.download_pdf, name='download_pdf'),


]