import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Juridictions(models.Model):
    idJuridiction = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)
    name = models.TextField('juridiction')
    address = models.CharField('privilege', max_length=200, null=True, blank=True)
    phone = models.CharField('telephone', max_length=200, null=True, blank=True)
    typeTribunal = models.CharField('type de tribunal', max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return self.name



class Files(models.Model):
    idFile = models.UUIDField(default=uuid.uuid4, editable=False)
    originalName = models.TextField('nom original')
    path = models.TextField('path')
    

