from django.contrib import admin
from .models import Account, Notification, Signature

# Register your models here.
admin.site.register(Account)
admin.site.register(Signature)
admin.site.register(Notification)