from django import forms
from . models import Roles,AffaireRoles,Enrollement
from django.forms import inlineformset_factory
from .models import Decisions
from .models import MessageDefilant

class MessageForm(forms.ModelForm):
    class Meta:
        model = MessageDefilant
        fields = ['contenu', 'actif']
        widgets = {
            'contenu': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'actif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class RoleForm(forms.ModelForm):
    class Meta: 
        model = Roles   
        fields = ('juridiction','section','president','juge','greffier','dateEnreg','typeAudience','assesseur','assesseur1','assesseur2','conseillers','ministerePublic','procureurMilitaire','subtituts')

class RoleAffaireForm(forms.ModelForm):
    class Meta: 
        model = AffaireRoles   
        fields =('numOrdre','numRg','objet','demandeurs','defendeurs','appelants','intimes','partieCiviles','civileResponsables','numAffaire','mandatDepot','natureInfraction','prevenus','detention','prevention')  
        widgets = {
            'numOrdre': forms.NumberInput(attrs={'class': 'form-control','required': True}),
            'numRg': forms.TextInput(attrs={'class': 'form-control','required': True, 'readonly': True}),
            'demandeurs': forms.Textarea(attrs={'class': 'form-control','required': True,'rows': 2}),
            'defendeurs': forms.Textarea(attrs={'class': 'form-control','required': True,'rows': 2}),
            'appelants': forms.Textarea(attrs={'class': 'form-control','required': True,'rows': 2}),
            'intimes': forms.Textarea(attrs={'class': 'form-control','required': True,'rows': 2}),
            'partieCiviles': forms.Textarea(attrs={'class': 'form-control','required': True,'rows': 2}),
            'civileResponsables': forms.Textarea(attrs={'class': 'form-control','required': True,'rows': 2}),
            'numAffaire': forms.TextInput(attrs={'class': 'form-control','required': True, 'readonly': True}),
            'mandatDepot': forms.Textarea(attrs={'class': 'form-control','required': True,'rows': 2}),
            'detention': forms.Textarea(attrs={'class': 'form-control','required': True,'rows': 2}),
            'prevention': forms.Textarea(attrs={'class': 'form-control','required': True,'rows': 2}),
            'natureInfraction': forms.Textarea(attrs={'class': 'form-control','required': True,'rows': 2}),
            'prevenus': forms.Textarea(attrs={'class': 'form-control','required': True,'rows': 2}),
            'objet': forms.Textarea(attrs={'class': 'form-control','required': True,'rows': 2}),
        }
AffaireFormSet = inlineformset_factory(Roles,AffaireRoles, form=RoleAffaireForm, extra=1, can_delete=True,can_delete_extra=True)


class EnrollementForm(forms.ModelForm):
    class Meta: 
        model = Enrollement
        fields =('juridiction','numOrdre','numAffaire','section','numRg','objet','demandeurs','defendeurs','juridiction','typeAudience','dateEnrollement','dateAudience')  
        widgets = {
            'numOrdre': forms.NumberInput(attrs={'class': 'form-control','required': True, 'value': 1}),
            'numRg': forms.TextInput(attrs={'class': 'form-control','required': True}),
            'demandeurs': forms.Textarea(attrs={'class': 'form-control','required': True,'rows': 2}),
            'defendeurs': forms.Textarea(attrs={'class': 'form-control','required': True,'rows': 2}),
            'numAffaire': forms.TextInput(attrs={'class': 'form-control','required': True, 'readonly': True}),
            'objet': forms.Textarea(attrs={'class': 'form-control','required': True,'rows': 2}),
            'dateEnrollement':forms.DateInput(attrs={'type':'date','class': 'form-control', 'required': True}),
            'dateAudience':forms.DateInput(attrs={'type':'date','class': 'form-control', 'required': True}),
        }

class DecisionsForm(forms.ModelForm):
    class Meta:
        model = Decisions
        fields = [
            'affaire', 'decision', 'typeDecision', 'objet', 'section',
            'president', 'greffier', 'dateDecision', 'dispositif',
            'prochaineAudience'
        ]
        widgets = {
            'decision': forms.Textarea(attrs={'class': 'form-control', 'cols':'30', 'rows':'5', 'required':'true', 'readonly':'true', 'style': 'color: gray; font-style: italic;'}),
            'typeDecision': forms.Select(attrs={'class': 'form-control', 'required':'true', 'id':'typeDecision'}),
            'objet': forms.Textarea(attrs={'class': 'form-control'}),
            'president': forms.TextInput(attrs={'class': 'form-control', 'required':'true'}),
            'greffier': forms.TextInput(attrs={'class': 'form-control', 'required':'true'}),
            'dispositif': forms.Textarea(attrs={'class': 'form-control', 'cols':'30', 'rows':'3'}),
            'dateDecision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required':'true'}),
            'prochaineAudience': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required':'true', 'id':'prochaineAudience'}),
        }