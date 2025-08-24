from django import forms
from .models import (
    Rccm, Formalite, PersonnePhysique, Foyer_personne_physique, 
    EtablissementPersonne, EtablissementSecondairePersonne, PersonnePhysiqueEngager, GerantPersonne, ActivitesAnterieuresPersonne,Declaration, OptionDeclaration,  PersonneMorale, EtablissementMorale, EtablissementSecondaireMorale,
    AssociesMorale, GerantMorale, CommissaireComptesMorale
)


# Personne morale
class PersonneMoraleForm(forms.ModelForm):
    class Meta:
        model = PersonneMorale
        fields = '__all__'
        widgets = {
            'denomination': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dénomination', 'id': 'denomination'}),
            'nomCommercial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom commercial', 'id': 'nomCommercial'}),
            'sigle': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Sigle', 'id': 'sigle'}),
            'siege': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Siège', 'id': 'siege'}),
            'rccmSiege': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RCCM du siège', 'id': 'rccmSiege'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Adresse', 'rows': 2, 'id': 'adresse'}),
            'formeJuridique': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Forme juridique', 'id': 'formeJuridique'}),
            'capitalSocial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Capital social', 'id': 'capitalSocial'}),
            'dontNumeraires': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dont numéraires', 'id': 'dontNumeraires'}),
            'dontNature': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dont en nature', 'id': 'dontNature'}),
            'duree': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Durée (en années)', 'id': 'duree'}),
        }

class EtablissementMoraleForm(forms.ModelForm):
    class Meta:
        model = EtablissementMorale
        fields = '__all__'
        widgets = {
            'activite': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Activité principale', 'id': 'activite'}),
            'dateDebut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'dateDebut'}),
            'nombreSalarierPrevu': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de salariés prévu', 'id': 'nombreSalarierPrevu'}),
            'etablissement': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Établissement principal ou succursale', 'id': 'etablissement'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Adresse de l\'établissement', 'rows': 2, 'id': 'adresse'}),
            'origine': forms.Select(attrs={'class': 'form-control', 'id': 'origine'}),
            'prenomPrecedentExploitant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom précédent exploitant', 'id': 'prenomPrecedent'}),
            'nomPrecedentExploitant': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom précédent exploitant', 'id': 'nomPrecedent'}),
            'banqueApport': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Loueur de fonds ou banque d\'apport', 'id': 'banqueApport'}),
        }

class EtablissementSecondaireMoraleForm(forms.ModelForm):
    class Meta:
        model = EtablissementSecondaireMorale
        fields = '__all__'
        widgets = {
            'existance': forms.Select(attrs={'class': 'form-control', 'id': 'existance'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Adresse', 'rows': 2, 'id': 'adresseSecondaire'}),
            'activite': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Activité secondaire', 'rows': 2, 'id': 'activiteSecondaire'}),
        }

class AssociesMoraleForm(forms.ModelForm):
    class Meta:
        model = AssociesMorale
        fields = '__all__'
        widgets = {
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom', 'id': 'associePrenom'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom', 'id': 'associeNom'}),
            'dateNaissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'dateNaissanceAssocie'}),
            'lieuNaissance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lieu de naissance', 'id': 'lieuNaissanceAssocie'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Adresse', 'rows': 2, 'id': 'adresseAssocie'}),
        }

class GerantMoraleForm(forms.ModelForm):
    class Meta:
        model = GerantMorale
        fields = '__all__'
        widgets = {
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom', 'id': 'gerantPrenom'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom', 'id': 'gerantNom'}),
            'dateNaissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'dateNaissanceGerant'}),
            'lieuNaissance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lieu de naissance', 'id': 'lieuNaissanceGerant'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Adresse', 'rows': 2, 'id': 'adresseGerant'}),
            'fonction': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fonction', 'id': 'fonctionGerant'}),
        }

class CommissaireComptesMoraleForm(forms.ModelForm):
    class Meta:
        model = CommissaireComptesMorale
        fields = '__all__'
        widgets = {
            'prenom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom', 'id': 'commissairePrenom'}),
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom', 'id': 'commissaireNom'}),
            'dateNaissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'id': 'dateNaissanceCommissaire'}),
            'lieuNaissance': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lieu de naissance', 'id': 'lieuNaissanceCommissaire'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Adresse', 'rows': 2, 'id': 'adresseCommissaire'}),
            'fonction': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Fonction', 'id': 'fonctionCommissaire'}),
        }
# End Personne morale

class ActivitesAnterieuresPersonneForm(forms.ModelForm):
    class Meta:
        model = ActivitesAnterieuresPersonne
        fields = '__all__'
        widgets = {
            'activite_precedente': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'activite_precedente'
            }),
            'type_activite': forms.Select(attrs={
                'class': 'form-control',
                'id': 'type_activite'
            }),
            'details_autre_activite': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Détails sur l'autre activité",
                'id': 'details_autre_activite'
            }),
            'periode_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'month',  # Pour saisir mois + année
                'id': 'periode_fin'
            }),
            'rccm_precedent': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "RCCM précédent",
                'id': 'rccm_precedent'
            }),
            'etablissement_principal': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Établissement principal",
                'rows': 2,
                'id': 'etablissement_principal'
            }),
            'etablissements_secondaires': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Établissements secondaires",
                'rows': 2,
                'id': 'etablissements_secondaires'
            }),
            'rccm_principal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "RCCM principal",
                'id': 'rccm_principal'
            }),
            'adresse': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Adresse géographique et postale",
                'rows': 2,
                'id': 'adresse'
            }),
        }



class RccmForm(forms.ModelForm):
    class Meta:
        model = Rccm
        fields = ['typeRccm', 'numeroRccm', 'dateEnreg', 'rccm_file']
        widgets = {
            'typeRccm': forms.Select(attrs={
                'class': 'form-control',
                'id': 'typeRccm',
                'required': True
            }),

            'numeroRccm': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le numéro RCCM',
                'id': 'numeroRccm',
                'required': True
            }),

            'dateEnreg': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'id': 'dateEnreg',
                    'required': True
                },
                format='%Y-%m-%d'
            ),

            'rccm_file': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'id': 'rccmFile',
                'required': True
            }),
        }


# Form for Formalite model

class FormaliteForm(forms.ModelForm):
    declarationModificative = forms.ModelMultipleChoiceField(
        queryset=Declaration.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control col-md-6',
            'id': 'declarationModificative',
            'multiple': 'multiple'  # important !
        }),
        required=False,
        label="Déclaration modificative"
    )

    optionDeclaration = forms.ModelMultipleChoiceField(
        queryset=OptionDeclaration.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control col-md-6',
            'id': 'optionDeclaration',
            'multiple': 'multiple'
        }),
        required=False,
        label="Options déclaration"
    )


    class Meta:
        model = Formalite
        fields = [
            'typeRccm', 'numeroFormalite', 'typeFormalite',
            'declarationModificative', 'optionDeclaration', 'dateModification',
        ]

        widgets = {
            'typeRccm': forms.Select(attrs={'class': 'form-select', 'required': True, 'id': 'typeRccm'}),
            'numeroFormalite': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Numéro Formalité', 
                'required': True, 
                'id': 'numeroFormalite'
            }),
           
            'typeFormalite': forms.Select(attrs={
                'class': 'form-select', 
                'id': 'typeFormalite',
                'required': True, 
            }),

            'dateModification': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date', 
                'required': True, 
                'id': 'dateModification'
            },  format='%Y-%m-%d'),
            
           
          
        }

def __init__(self, *args, **kwargs):
    super(FormaliteForm, self).__init__(*args, **kwargs)
    
    if self.instance and self.instance.pk:
        if not self.instance.numeroFormalite:
            self.initial['numeroFormalite'] = ''
        if not self.instance.dateModification:
            self.initial['dateModification'] = None
        if not self.instance.declarationModificative:
            self.initial['declarationModificative'] = []
        if not self.instance.optionDeclaration:
            self.initial['optionDeclaration'] = []


        # Optionnel : filtrer dynamiquement les optionDeclaration selon déclarationModificative
        # (à activer en JS ou manuellement ici selon ton besoin)


# Form for PersonnePhysique model
class PersonnePhysiqueForm(forms.ModelForm):
    class Meta:
        model = PersonnePhysique
        # Define fields for managing personal details
        fields = [
            'formalite', 'titreCivil', 'prenom', 'nom', 'dateNaissance', 
            'lieuNaissance', 'nationnalite', 'adressePostale', 'telephone', 'domicile', 
            'ville', 'quartier', 'autrePrecision', 'coordonneesElectro', 'situationMatrimoniale','champsRectifier'
            
        ]
        widgets = {
            'formalite': forms.Select(attrs={'class': 'form-control', 'id': 'formalite'}),
            'titreCivil': forms.Select(attrs={'class': 'form-control', 'required': True, 'id': 'titreCivil'}),
            
            # Text input for names and nationalities
            'prenom': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Prénom', 
                'required': True, 
                'id': 'prenom'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nom', 
                'required': True, 
                'id': 'nom'
            }),
            'nationnalite': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nationalité', 
                'required': True, 
                'id': 'nationnalite'
            }),

            # Date input for date of birth
            'dateNaissance': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date', 
                'placeholder': 'YYYY-MM-DD', 
                'required': True, 
                'id': 'dateNaissance'
            }, format='%Y-%m-%d'),

            # Text inputs for location and address details
            'lieuNaissance': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Lieu de naissance', 
                'required': True, 
                'id': 'lieuNaissance'
            }),
            'adressePostale': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Adresse complète', 
                'id': 'adressePostale'
            }),
            'ville': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ville', 
                'required': True, 
                'id': 'ville'
            }),
            'quartier': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Quartier', 
                'required': True, 
                'id': 'quartier'
            }),
            'autrePrecision': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Autres précisions', 
                'id': 'autrePrecision'
            }),

            # Phone and contact details
            'telephone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Numéro de téléphone', 
                'type': 'tel', 
                'required': True, 
                'id': 'telephone'
            }),
            'domicile': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Domicile', 
                'required': True, 
                'id': 'domicile'
            }),
             'champsRectifier': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Champs à rectifier', 
                'required': False,
                'id': 'champsRectifier'
            }),
            'coordonneesElectro': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Email', 
                'id': 'coordonneesElectro'
            }),

            # Dropdown for marital status
            'situationMatrimoniale': forms.Select(attrs={
                'class': 'form-control', 
                'required': True, 
                'id': 'situationMatrimoniale'
            }),
        }

# Form for Foyer_personne_physique model
class FoyerPersonnePhysiqueForm(forms.ModelForm):
    class Meta:
        model = Foyer_personne_physique
        # Fields related to person's marital details
        fields = [
            'personnePhysique', 'conjoint', 'nomComplet', 'dateLieuMariage', 
            'optionMatrimoniale', 'regimeMatrimoniale', 'demandeSeparationBien'
        ]

# Form for Etablissement model

class EtablissementPersonneForm(forms.ModelForm):
    class Meta:
        model = EtablissementPersonne
        fields = [
            'formalite', 'sigle', 'nomCommercial', 'rccm', 'denomination', 'ancienDenomination',
            'mandataire', 'siegeSocial', 'activites', 'activitesAjouter', 'activitesSupprimer',
            'activitesActualiser', 'adresseEtablissement', 'ancienneAdresse', 'nouvelleAdresse'
        ]
        widgets = {
            'sigle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sigle',
                'id': 'sigle'
            }),
            'nomCommercial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom commercial',
                'id': 'nomCommercial'
            }),
            'rccm': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro RCCM',
                'id': 'rccm'
            }),
            'denomination': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dénomination',
                'id': 'denomination'
            }),
            'ancienDenomination': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ancienne dénomination',
                'id': 'ancienDenomination'
            }),
            'mandataire': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mandataire',
                'id': 'mandataire'
            }),
            'siegeSocial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Siège social',
                'id': 'siegeSocial'
            }),
            'activites': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Activités principales',
                'rows': 2,
                'id': 'activites'
            }),
            'activitesAjouter': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Activités ajoutées',
                'rows': 2,
                'id': 'activitesAjouter'
            }),
            'activitesSupprimer': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Activités supprimées',
                'rows': 2,
                'id': 'activitesSupprimer'
            }),
            'activitesActualiser': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Activités actualisées',
                'rows': 2,
                'id': 'activitesActualiser'
            }),
            'adresseEtablissement': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse de l\'établissement',
                'rows': 2,
                'id': 'adresseEtablissement'
            }),
            'ancienneAdresse': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ancienne adresse',
                'rows': 2,
                'id': 'ancienneAdresse'
            }),
            'nouvelleAdresse': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Nouvelle adresse',
                'rows': 2,
                'id': 'nouvelleAdresse'
            }),
        }

# Form for EtablissementSecondaire model

class EtablissementSecondairePersonneForm(forms.ModelForm):
    class Meta:
        model = EtablissementSecondairePersonne
        fields = [
            'formalite', 'sigle', 'nomCommercial', 'rccm', 'activites', 'activitesAjouter',
            'activitesSupprimer', 'activitesActualiser', 'autresActivites', 'adresseEtablissement',
            'ancienneAdresse', 'nouvelleAdresse'
        ]
        widgets = {
            'sigle': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sigle',
                'id': 'sigleSecondaire'
            }),
            'nomCommercial': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom commercial',
                'id': 'nomCommercialSecondaire'
            }),
            'rccm': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Numéro RCCM',
                'id': 'rccmSecondaire'
            }),
            'activites': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Activités principales',
                'rows': 2,
                'id': 'activitesSecondaire'
            }),
            'activitesAjouter': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Activités à ajouter',
                'rows': 2,
                'id': 'activitesAjouterSecondaire'
            }),
            'activitesSupprimer': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Activités à supprimer',
                'rows': 2,
                'id': 'activitesSupprimerSecondaire'
            }),
            'activitesActualiser': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Activités actualisées',
                'rows': 2,
                'id': 'activitesActualiserSecondaire'
            }),
            'autresActivites': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Autres activités',
                'rows': 2,
                'id': 'autresActivitesSecondaire'
            }),
            'adresseEtablissement': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Adresse de l\'établissement',
                'rows': 2,
                'id': 'adresseEtablissementSecondaire'
            }),
            'ancienneAdresse': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Ancienne adresse',
                'rows': 2,
                'id': 'ancienneAdresseSecondaire'
            }),
            'nouvelleAdresse': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Nouvelle adresse',
                'rows': 2,
                'id': 'nouvelleAdresseSecondaire'
            }),
        }


# Form for PersonnePhysiqueEngager model
class PersonnePhysiqueEngagerForm(forms.ModelForm):
    class Meta:
        model = PersonnePhysiqueEngager
        # Fields for managing person's engagement information
        fields = [
            'formalite', 'prenom', 'nom', 'dateNaissance', 'lieuNaissance', 
            'nationnalite', 'domicile', 'modeDomicilier', 'objetModification', 'dateModification2', 'statut',
        ]
        widgets = {
            # Text input for prenom and nom
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le prénom',
                'id': 'prenom2'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le nom',
                'id': 'nom2'
            }),

            # Date picker for dateNaissance
            'dateNaissance': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'dateNaissance2'
            }, format='%Y-%m-%d'),

            # Text input for lieuNaissance
            'lieuNaissance': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le lieu de naissance',
                'id': 'lieuNaissance2'
            }),

            # Dropdown for nationnalite
            'nationnalite': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sélectionnez la nationalité',
                'id': 'nationnalite2'
            }),

            # Text input for domicile
            'domicile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez le domicile',
                'id': 'domicile2'
            }),

            # Dropdown or radio buttons for modeDomicilier
            'modeDomicilier': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Sélectionnez le mode de domiciliation',
                'id': 'modeDomicilier'
            }),

            # Textarea for objetModification
            'objetModification': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Décrivez l\'objet de la modification',
                'id': 'objetModification'
            }),

            # Date picker for dateModification
            'dateModification2': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'id': 'dateModification2'
            }, format='%Y-%m-%d'),

             'statut': forms.Select(attrs={
                'class': 'form-control w-50', 
                'required': False, 
                'id': 'statut'
            }),
        }


# Form for Gerant model

class GerantPersonneForm(forms.ModelForm):
    class Meta:
        model = GerantPersonne
        fields = [
            'formalite', 'titreCivil', 'prenom', 'nom', 'typeDemande'
        ]
        widgets = {
            'titreCivil': forms.Select(attrs={
                'class': 'form-control',
                'id': 'titreCivilGerant',
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom',
                'id': 'gerantPrenomPersonne',
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom',
                'id': 'gerantNomPersonne',
            }),
            'typeDemande': forms.Select(attrs={
                'class': 'form-control',
                'id': 'typeDemandeGerant',
            }),
        }


class PDFUploadForm(forms.Form):
    type_rccm = forms.ChoiceField(
        choices=[('', '--------------'), ('PERSONNE PHYSIQUE', 'Personne physique'), ('PERSONNE MORALE', 'Personne morale')],  # Remplacez par les choix appropriés, par exemple : [('option1', 'Option 1'), ('option2', 'Option 2')]
        widget=forms.Select(attrs={'class': 'form-select mb-4', 'id': 'typeRccm'}),
        required=True
    )

    pdf_file = forms.FileField(
        label="Importez ici le document scanné ",
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control mb-4', 'id':'', 'accept': 'application/pdf'})
    )

    result_ocr = forms.CharField(
        label="Texte dispositif",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'id': 'ocrResult',
            'rows': 6,
            'cols': 40,
            'readonly': True,  # Rend le champ non modifiable
            'style': 'background-color: #e9ecef; cursor: not-allowed;'  # Grise le champ et change le curseur
        })
    )


class PDFUploadSignature(forms.Form):
   
    formaliteSignee = forms.FileField(
        label="Importez ici le document scanné ",
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control mb-4', 'id':'upload_signature', 'accept': 'application/pdf'})
    )



