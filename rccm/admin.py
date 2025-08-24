from django.contrib import admin

# Register your models here.
from .models import Rccm, Formalite, Declaration, OptionDeclaration

# Register your models here.
admin.site.register(Rccm)
admin.site.register(Formalite)
admin.site.register(Declaration)
admin.site.register(OptionDeclaration)