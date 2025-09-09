from django.contrib import admin

from role.models import AffaireRoles, DecisionHistory, Decisions, Enrollement, EnrollementHistory, MessageDefilant, Roles, SuivreAffaire


admin.site.register(Roles)
admin.site.register(AffaireRoles)
admin.site.register(Decisions)
admin.site.register(DecisionHistory)
admin.site.register(SuivreAffaire)
admin.site.register(Enrollement)
admin.site.register(EnrollementHistory)
admin.site.register(MessageDefilant)
