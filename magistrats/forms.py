from django import forms
from . models import Presidents,Conseillers,Assesseurs
from django.forms import inlineformset_factory

class PresidentForm(forms.ModelForm):
    class Meta: 
        model = Presidents   
        fields =('prenomNom','chambre','juridiction') 

class ConseillerForm(forms.ModelForm):
    class Meta: 
        model = Conseillers   
        fields =('prenomNom','juridiction')  

class AssesseurForm(forms.ModelForm):
    class Meta: 
        model = Assesseurs   
        fields =('prenomNom','juridiction')  
