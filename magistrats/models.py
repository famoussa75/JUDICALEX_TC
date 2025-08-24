from django.db import models
from _base.models import Juridictions
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# Create your models here.

class Presidents(models.Model):
    TYPE_CHAMBRE = (
        ("Prémière chambre civile,commerciale et sociale", "Prémière chambre civile, commerciale et sociale"),
        ("Deuxième chambre civile,commerciale et sociale", "Deuxième chambre civile, commerciale et sociale"),
        ("Troisième chambre civile,commerciale et sociale", "Troisième chambre civile, commerciale et sociale"),
        ("Quatrième chambre civile,commerciale et sociale", "Quatrième chambre civile, commerciale et sociale"),
        ("Chambre administrative civile,commerciale et sociale", "Chambre administrative civile, commerciale et sociale"),
        ("Prémière chambre pénale", "Prémière chambre pénale"),
        ("Deuxième chambre pénale", "Deuxième chambre pénale"),
        ("Non définie","Non définie"),
    )
    prenomNom = models.TextField('Prenom et Nom')
    chambre = models.TextField(null=True, blank=True,verbose_name=_('Chambre'))
    juridiction = models.ForeignKey(Juridictions,blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Juridiction'))
    created_at = models.DateTimeField(null=True, blank=True,auto_now=True, verbose_name=_('Date de creation')) 

    def __str__(self):
        return str(self.id)

class Conseillers(models.Model):
    prenomNom = models.TextField('Prenom et Nom')
    juridiction = models.ForeignKey(Juridictions,blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Juridiction'))
    created_at = models.DateTimeField(null=True, blank=True,auto_now=True, verbose_name=_('Date de creation'))

    def __str__(self):
        return str(self.id)


class Assesseurs(models.Model):
    prenomNom = models.TextField('Prenom et Nom')
    juridiction = models.ForeignKey(Juridictions,blank=True, null=True, on_delete=models.CASCADE, verbose_name=_('Juridiction'))
    created_at = models.DateTimeField(null=True, blank=True,auto_now=True, verbose_name=_('Date de creation')) 

    def __str__(self):
        return str(self.id)
