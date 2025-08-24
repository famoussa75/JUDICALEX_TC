import uuid
from django.db import models
from django.utils import timezone
from _base.models import Juridictions
from account.models import Account
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Roles(models.Model):

    TYPE_AUDIENCE = (
        ("Refere", "Référé"),
        ("Fond", "Fond"),
    )

    TYPE_SECTION = (
            ("Premiere-Section", "Prémière Section"),
            ("Deuxieme-Section", "Deuxième Section"),
            ("Troisieme-Section", "Troisième Section"),
            ("Quatrieme-Section", "Quatrième Section"),
            ("Cinquieme-Section", "Cinquième Section"),
            ("Section-Presidentielle", "Section Présidentielle"),
    )

    STATUT = (
        ("En-attente", "En attente"),
        ("Valider", "Validé"),
    )

    idRole = models.UUIDField(default=uuid.uuid4, editable=False)
    section = models.TextField(null=True, blank=True,choices=TYPE_SECTION,verbose_name=_('Section'))
    president = models.TextField(null=True, blank=True,verbose_name=_('President(e)'))
    juge = models.TextField(null=True, blank=True,verbose_name=_('Juge consulaire'))
    assesseur = models.TextField(null=True, blank=True,verbose_name=_('Assesseur'))
    assesseur1 = models.TextField(null=True, blank=True,verbose_name=_('1er Ass'))
    assesseur2 = models.TextField(null=True, blank=True,verbose_name=_('2ème Ass'))
    conseillers = models.TextField(null=True, blank=True,verbose_name=_('Conseillers'))
    ministerePublic = models.TextField(null=True, blank=True,verbose_name=_('Ministère public'))
    greffier = models.TextField(null=True, blank=True,verbose_name=_('Greffier(e)'))
    typeAudience = models.TextField(null=True, blank=True,choices=TYPE_AUDIENCE,verbose_name=_('Type d\'audience'))
    dateEnreg =  models.DateField(null=True, blank=True,verbose_name=_('Date d\'enregistrement'))
    filePath = models.TextField(null=True, blank=True,verbose_name=_('Piece jointe'))
    procureurMilitaire = models.TextField(null=True, blank=True, verbose_name=_('Procureur Militaire'))
    subtituts = models.TextField(null=True, blank=True, verbose_name=_('Subtitut')) 
    juridiction = models.ForeignKey(Juridictions,blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Juridiction'))
    created_at = models.DateTimeField(null=True, blank=True,auto_now=True, verbose_name=_('Date de creation'))
    created_by = models.ForeignKey(Account,blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Creer par'))
    statut = models.TextField(null=True, blank=True,choices=STATUT, default="En-attente", verbose_name=_('Statut'))
 


    def __str__(self):
        return str(self.idRole)
   
class AffaireRoles(models.Model):

   
    idAffaire = models.UUIDField(default=uuid.uuid4, editable=False)
    numOrdre = models.IntegerField(null=False, blank=False, verbose_name=_('Numéro d\'ordre'))
    numRg = models.CharField(max_length=200,null=True, blank=True, verbose_name=_('Numéro Rg'))
    numAffaire = models.CharField(max_length=200,null=True, blank=True, verbose_name=_('Numéro Affaire'))
    objet = models.TextField(null=True, blank=True, verbose_name=_('Objet'))
    mandatDepot = models.TextField(null=True, blank=True, verbose_name=_('Mandats de Dépôt'))
    detention = models.TextField(null=True, blank=True, verbose_name=_('Detention'))
    prevention = models.TextField(null=True, blank=True, verbose_name=_('Prevention'))
    natureInfraction = models.TextField(null=True, blank=True, verbose_name=_('Nature des infractions'))
    decision = models.TextField(null=True, blank=True, verbose_name=_('Décision'))
    prevenus = models.TextField(null=True, blank=True, verbose_name=_('Prévenus'))
    demandeurs = models.TextField(null=True, blank=True, verbose_name=_('Demandeurs'))
    defendeurs = models.TextField(null=True, blank=True, verbose_name=_('Défendeurs'))
    appelants = models.TextField(null=True, blank=True, verbose_name=_('Appelants'))
    intimes = models.TextField(null=True, blank=True, verbose_name=_('Intimés'))
    partieCiviles = models.TextField(null=True, blank=True, verbose_name=_('Parties civiles'))
    civileResponsables = models.TextField(null=True, blank=True, verbose_name=_('Civiles Responsables'))
    role = models.ForeignKey(Roles, on_delete=models.CASCADE,null=True, blank=True, verbose_name=_('Role'))
    created_at = models.DateTimeField(auto_now=True, verbose_name=_('Date creation'))
    created_by = models.ForeignKey(Account,blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Creer par'))


class Decisions(models.Model):

    TYPE_DECISION = (
        ("Renvoi", "Renvoi"),
        ("Mise-en-delibere", "Mise en délibéré"),
        ("Vide-du-delibere", "Vidé du délibéré"),
        ("Delibere-proroge", "Délibéré prorogé"),
        ("Radiation", "Radiation"),
        ("Renvoi-sine-die", "Renvoi sine die"),
        ("Affectation", "Affectation"),
        ("Autre", "Autre"),
    )

    TYPE_SECTION = (
            ("Premiere-Section", "Prémière Section"),
            ("Deuxieme-Section", "Deuxième Section"),
            ("Troisieme-Section", "Troisième Section"),
            ("Quatrieme-Section", "Quatrième Section"),
            ("Cinquieme-Section", "Cinquième Section"),
            ("Section-Presidentielle", "Section Présidentielle"),
    )

    STATUT = (
        ("Creer", "Créée"),
        ("Modifier", "Modifiée"),
        ("Annuler", "Annulée"),
    )

     
    idDecision = models.UUIDField(default=uuid.uuid4, editable=False)
    juridiction = models.ForeignKey(Juridictions,blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Juridiction'))
    affaire = models.ForeignKey(AffaireRoles, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Affaire_decision'))
    decision = models.TextField(null=True, blank=True, verbose_name=_('Décision'))
    section = models.TextField(null=True, blank=True,choices=TYPE_SECTION,verbose_name=_('Section'))
    typeDecision = models.TextField(null=True, blank=True,choices=TYPE_DECISION,verbose_name=_('Type decision'))
    objet = models.TextField(null=True, blank=True, verbose_name=_('Objet'))
    president = models.TextField(null=True, blank=True, verbose_name=_('President'))
    greffier = models.TextField(null=True, blank=True, verbose_name=_('Greffier'))
    dateDecision = models.DateField(null=True, blank=True, verbose_name=_('Date de décision'))
    dispositif = models.TextField(null=True, blank=True, verbose_name=_('Dispositif'))
    prochaineAudience = models.DateField(null=True, blank=True, verbose_name=_('Prochaine audience'))
    statut = models.TextField(null=True, blank=True,choices=STATUT, default="Creer", verbose_name=_('Statut'))
    created_at = models.DateTimeField(auto_now=True, verbose_name=_('Date creation'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Date modification'))
    created_by = models.ForeignKey(Account,blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Creer par'))

class DecisionHistory(models.Model):
    original = models.ForeignKey(Decisions, on_delete=models.CASCADE, related_name="historiques")
    juridiction = models.ForeignKey(Juridictions, blank=True, null=True, on_delete=models.CASCADE)
    affaire = models.ForeignKey(AffaireRoles, on_delete=models.CASCADE, null=True, blank=True)
    decision = models.TextField(null=True, blank=True)
    section = models.TextField(null=True, blank=True, choices=Decisions.TYPE_SECTION)
    typeDecision = models.TextField(null=True, blank=True, choices=Decisions.TYPE_DECISION)
    objet = models.TextField(null=True, blank=True)
    president = models.TextField(null=True, blank=True)
    greffier = models.TextField(null=True, blank=True)
    dateDecision = models.DateField(null=True, blank=True)
    dispositif = models.TextField(null=True, blank=True)
    prochaineAudience = models.DateField(null=True, blank=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(Account, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Historique de {self.original} - {self.created_at.strftime('%d/%m/%Y %H:%M')}"


class SuivreAffaire(models.Model):
    id = models.AutoField(primary_key=True)
    idSuivre = models.UUIDField(default=uuid.uuid4, editable=False)
    affaire = models.ForeignKey(AffaireRoles, on_delete=models.CASCADE, null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Suiveur'))
    juridiction = models.ForeignKey(Juridictions,blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Juridiction'))
    created_at = models.DateTimeField(auto_now=True, verbose_name=_('Date de suivi'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Date modification suivi'))



class Enrollement(models.Model):

    TYPE_AUDIENCE = (
        ("Standard", "Standard"),
        ("Refere", "Référé"),
        ("Fond", "Fond"),
        ("Civile", "Civile"),
        ("Correctionnelle", "Correctionnelle"),
        ("Criminelle", "Criminelle"),
    )

    TYPE_SECTION = (
        ("Premiere-Section", "Prémière Section"),
        ("Deuxieme-Section", "Deuxième Section"),
        ("Troisieme-Section", "Troisième Section"),
        ("Quatrieme-Section", "Quatrième Section"),
        ("Cinquieme-Section", "Cinquième Section"),
        ("Section-Presidentielle", "Section Présidentielle"),
    )

    STATUT = (
        ("Creer", "Créée"),
        ("Modifier", "Modifiée"),
        ("Annuler", "Annulée"),
    )

    idAffaire = models.UUIDField(default=uuid.uuid4, editable=False)
    numOrdre = models.IntegerField(null=False, blank=False, verbose_name=_('Numéro d\'ordre'))
    numRg = models.CharField(max_length=200,null=True, blank=True, verbose_name=_('Numéro Rg'))
    numAffaire = models.CharField(max_length=200,null=True, blank=True, verbose_name=_('Numéro Affaire'))
    objet = models.TextField(null=True, blank=True, verbose_name=_('Objet'))
    decision = models.TextField(null=True, blank=True, verbose_name=_('Décision'))
    demandeurs = models.TextField(null=True, blank=True, verbose_name=_('Demandeurs'))
    defendeurs = models.TextField(null=True, blank=True, verbose_name=_('Défendeurs'))
    dateEnrollement = models.DateField(null=True, blank=True, verbose_name=_('Date d\'enrollement'))
    dateAudience = models.DateField(null=True, blank=True, verbose_name=_('Date d\'audience'))
    juridiction = models.ForeignKey(Juridictions,blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Juridiction'))
    typeAudience = models.TextField(null=True, blank=True,choices=TYPE_AUDIENCE,verbose_name=_('Type d\'audience'))
    section = models.TextField(null=True, blank=True,choices=TYPE_SECTION,verbose_name=_('Section'))
    created_at = models.DateTimeField(auto_now=True, verbose_name=_('Date creation'))
    created_by = models.ForeignKey(Account,blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Creer par'))
    statut = models.TextField(null=True, blank=True,choices=STATUT, default="Creer", verbose_name=_('Statut'))
    motifAnnulation = models.TextField(null=True, blank=True, verbose_name=_('Motif annulation'))


class EnrollementHistory(models.Model):
    original = models.ForeignKey('Enrollement', on_delete=models.CASCADE, related_name="histories")

    # On recopie les mêmes champs que dans Enrollement
    numOrdre = models.IntegerField()
    numRg = models.CharField(max_length=200, null=True, blank=True)
    numAffaire = models.CharField(max_length=200, null=True, blank=True)
    objet = models.TextField(null=True, blank=True)
    decision = models.TextField(null=True, blank=True)
    demandeurs = models.TextField(null=True, blank=True)
    defendeurs = models.TextField(null=True, blank=True)
    dateEnrollement = models.DateField(null=True, blank=True)
    dateAudience = models.DateField(null=True, blank=True)
    juridiction = models.ForeignKey(Juridictions, blank=True, null=True, on_delete=models.SET_NULL)
    typeAudience = models.TextField(null=True, blank=True, choices=Enrollement.TYPE_AUDIENCE)
    section = models.TextField(null=True, blank=True, choices=Enrollement.TYPE_SECTION)
    statut = models.TextField(null=True, blank=True, choices=Enrollement.STATUT, default="Creer")
    motifAnnulation = models.TextField(null=True, blank=True)

    # Infos de l’historique
    modified_at = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(Account, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-modified_at']


class MessageDefilant(models.Model):
    contenu = models.TextField("Contenu du message")
    actif = models.BooleanField("Afficher ce message", default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contenu[:50]