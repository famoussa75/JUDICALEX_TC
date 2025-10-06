from django.urls import path, include
from . import views

urlpatterns = [
     path('', views.index, name='role.index'),
     path("backoffice-data/", views.backoffice_data, name="backoffice_data"),
     path('roles/', views.listRole, name='role.liste'),
     path('roles/export-excel/', views.export_roles_excel, name='role.export_excel'),
     path('roles/export-pdf/', views.export_roles_pdf, name='role.export_pdf'),
     path('roles/valide/<int:pk>/', views.valide_role, name='role.valider'),
     path('affaires/', views.listAffaire, name='role.affaires'),
     path('affaires/details/<idAffaire>', views.detailAffaire, name='affaires.details'),
     path('plumitif/export/excel/', views.export_plumitifs_excel, name='plumitif.export_excel'),
     path('plumitif/export/pdf/', views.export_plumitifs_pdf, name='plumitif.export_pdf'),
     path('role_detail/export/excel/', views.export_roleDetail_excel, name='role_detail.export_excel'),
     path('decisions/export/pdf/', views.export_decisions_pdf, name='decisions.export_pdf'),
     path('decisions/export/excel/', views.export_decisions_excel, name='decisions.export_excel'),
     path('role_detail/export/pdf/', views.export_roleDetail_pdf, name='role_detail.export_pdf'),
     path('roles/update', views.updateRole, name='role.update'),
     path('roles/delete', views.deleteRole, name='role.delete'),
     path('decisions/delete', views.deleteDecision, name='decision.delete'),
     path('decisions/update/', views.update_decision, name='decision.update'),
     path('creation-role/', views.createRole, name='role.create'),
     path('enrollement/', views.listEnrollement, name='role.enrollement'),
     path('enrollement/list/', views.listEnrollementForAdmin, name='role.enrollementForAdmin'),
     path('affaires/<int:id>/cancel/', views.cancel_affaire, name='affaires.cancel'),
     path('affaires/edit/<idAffaire>', views.edit_affaire, name='affaires.edit'),
     path('enrollements/export/excel/', views.export_enrollements_excel, name='export_enrollements_excel'),
     path('enrollements/export/pdf/', views.export_enrollements_pdf, name='export_enrollements_pdf'),
     path('historique/enrollement/<int:pk>/', views.historique_modifications_enrollement, name='historique_modifications_enrollement'),
     path('historique/decisions/<int:pk>/', views.historique_modifications_decisions, name='historique_modifications_decisions'),
     path('creation-enrollement/', views.createEnrollement, name='role.createEnrollement'),
     path('details/<pk>', views.roleDetail, name='role.detail'),
     path('gestion-messages/', views.ges_message, name='ges_message'),
     path('gestion-messages/<int:pk>/<str:action>/', views.ges_message, name='gestion_messages_edit'),

     path('fetch-form/<selectedJuridiction>/<selectedType>/<selectedSection>/<dateRole>/', views.fetchForm, name='role.fetchForm'),
     path('fetch-form-enrollement/<selectedJuridiction>/<selectedType>/', views.fetchFormEnrollement, name='role.fetchFormEnrollement'),

     path('download-pdf/', views.download_pdf, name='download_pdf'),
     path('check-doublon/', views.check_doublon, name='check_doublon'),



]