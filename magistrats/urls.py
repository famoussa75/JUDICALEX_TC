from django.urls import path, include
from . import views

urlpatterns = [
     path('president/', views.president, name='magistrats.president'),
     path('president/<idPresident>/', views.president, name='magistrats.president'),
     path('president/delete/<idPresident>/', views.deletePresident, name='delete_president'),
     path('president/fetch-data/<idPresident>/', views.fetchPresident, name='president.fetchData'),

     path('conseillers/', views.conseiller, name='magistrats.conseiller'),
     path('conseillers/<idConseiller>/', views.conseiller, name='magistrats.conseiller'),
     path('conseillers/delete/<idConseiller>/', views.deleteConseiller, name='delete_conseiller'),
     path('conseillers/fetch-data/<idConseiller>/', views.fetchConseiller, name='conseillers.fetchData'),

     path('assesseurs/', views.assesseur, name='magistrats.assesseur'),
     path('assesseurs/<idAssesseur>/', views.assesseur, name='magistrats.assesseur'),
     path('assesseurs/delete/<idAssesseur>/', views.deleteAssesseur, name='delete_assesseur'),
     path('assesseurs/fetch-data/<idAssesseur>/', views.fetchAsseseur, name='assesseurs.fetchData'),

]