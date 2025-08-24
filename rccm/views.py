import datetime
import locale
import PyPDF2
from django.forms import modelformset_factory
from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction
from django.http import JsonResponse, Http404
import pdfplumber
from django.views.decorators.csrf import csrf_exempt
import json
from account.models import Account, Notification
from django.contrib.auth.hashers import check_password
from .models import *
from .forms import *
import re

import pytesseract
from PIL import Image
from django.core.files.storage import default_storage
from django.conf import settings

from pdf2image import convert_from_path
import os
from django.utils.text import slugify

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
import xlwt
from django.http import HttpResponse

from django.urls import reverse
from django.utils.html import strip_tags


# Dashboard
def index(request):
    return render(request, 'rccm/index.html')


# Modification
def modification(request):

    search_query = request.GET.get('search', '')
    type_formalite = request.GET.get('typeFormalite', '')

    formalites_list = Formalite.objects.all().order_by('-id')

    if search_query:
        formalites_list = formalites_list.filter(
        Q(numeroFormalite__icontains=search_query) |
        Q(denomination__icontains=search_query)
    )
    
     # Appliquer le filtre par type de formalité
    if type_formalite:
        formalites_list = formalites_list.filter(typeFormalite=type_formalite)
    

    paginator = Paginator(formalites_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'formalites': page_obj, 'page_obj': page_obj, 'search_query': search_query,}  

    return render(request, 'rccm/modification/index.html', context)



def detail(request, slug):
    url = request.build_absolute_uri()
    marquer_notification_lue(request, url)

    formalite = get_object_or_404(Formalite, slug=slug)
    rccm_type = formalite.rccm.typeRccm if formalite and formalite.rccm else None

    context = {'formalite': formalite}

    if rccm_type == "PERSONNE PHYSIQUE":
        context.update({
            'etablissement': EtablissementPersonne.objects.filter(formalite=formalite).first(),
            'personne_physique': PersonnePhysique.objects.filter(formalite=formalite).first(),
            'foyer_personne_physique': Foyer_personne_physique.objects.filter(formalite=formalite).first(),
            'etablissement_secondaire': EtablissementSecondairePersonne.objects.filter(formalite=formalite).first(),
            'personne_physique_engager': PersonnePhysiqueEngager.objects.filter(formalite=formalite),
            'gerant': GerantPersonne.objects.filter(formalite=formalite).first(),
        })

        template = 'rccm/modification/personne_physique/detail/single-formalite.html'

    elif rccm_type == "PERSONNE MORALE":
        context.update({
            'personne_morale': PersonneMorale.objects.filter(formalite=formalite).first(),
            'etablissement_morale': EtablissementMorale.objects.filter(formalite=formalite).first(),
            'etablissement_secondaire_morale': EtablissementSecondaireMorale.objects.filter(formalite=formalite).first(),
            'associes_morale': AssociesMorale.objects.filter(formalite=formalite),
            'gerants_morale': GerantMorale.objects.filter(formalite=formalite),
            'commissaires': CommissaireComptesMorale.objects.filter(formalite=formalite),
        })

        template = 'rccm/modification/personne_morale/detail/single-formalite.html'

    else:
        return render(request, 'rccm/modification/detail/invalide.html', {'message': "Type RCCM inconnu ou invalide."})

    return render(request, template, context)



def search_rccm(request):
    if  request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "GET":
        query = request.GET.get('query', '').strip()
        results = []

        if query:  # Vérifiez que le champ de recherche n'est pas vide
            results = Rccm.objects.filter(numeroRccm__icontains=query).values('numeroRccm','id')

        return JsonResponse({'results': list(results)}, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def rccm(request):

    rccms = Rccm.objects.all().order_by('-id')
    context = {'rccms':rccms}  
    return render(request, 'rccm/creation/list-rccm.html', context)

def rccm_detail(request, pk):

    rccm = Rccm.objects.filter(id=pk).first()
    formalites = Formalite.objects.filter(rccm=pk)
    last_formalite = Formalite.objects.filter(rccm=pk).last()
    context = {
                'formalites':formalites,
                'rccm':rccm,
                'last_formalite':last_formalite
              }  
    return render(request, 'rccm/creation/detail-rccm.html', context)


def formalite(request):
    
    rccmForm = RccmForm()
    formaliteForm = FormaliteForm()
    personnePhysiqueForm = PersonnePhysiqueForm()
    foyerPersonnePhysiqueForm = FoyerPersonnePhysiqueForm()
    etablissementPersonneForm = EtablissementPersonneForm()
    etablissementSecondaireForm = EtablissementSecondairePersonneForm()
    personnePhysiqueEngagerForm = PersonnePhysiqueEngagerForm()
    gerantForm = GerantPersonneForm()

    context = {
        'rccmForm':rccmForm,
        'formaliteForm':formaliteForm,
        'personnePhysiqueForm':personnePhysiqueForm,
        'foyerPersonnePhysiqueForm':foyerPersonnePhysiqueForm,
        'etablissementPersonneForm': etablissementPersonneForm,
        'etablissementSecondaireForm': etablissementSecondaireForm,
        'personnePhysiqueEngagerForm': personnePhysiqueEngagerForm,
        'gerantForm': gerantForm,
    }
    return render (request, 'rccm/modification/personne_physique/form/create.html', context)


def formaliteRapide(request, pk):
    # Récupérer l'objet RCCM
    rccm_instance = get_object_or_404(Rccm, pk=pk)
    type_rccm = rccm_instance.typeRccm

    # Formulaire RCCM (readonly ou non)
    rccmForm = RccmForm(instance=rccm_instance)

    # Dernière formalité liée au RCCM
    formalite_instance = Formalite.objects.filter(rccm=rccm_instance).last()
    formaliteForm = FormaliteForm(instance=formalite_instance)

    if type_rccm == "PERSONNE PHYSIQUE":
        formaliteForm.fields['declarationModificative'].queryset = Declaration.objects.filter(typeRccm='personne_physique')
    elif type_rccm == "PERSONNE MORALE":
        formaliteForm.fields['declarationModificative'].queryset = Declaration.objects.filter(typeRccm='personne_morale')

    # Vider certains champs pour la nouvelle formalité
    fields_to_clear = ['numeroFormalite', 'dateModification', 'typeFormalite', 'declarationModificative']
    for field in fields_to_clear:
        if field in formaliteForm.fields:
            formaliteForm.initial[field] = None

    # CONTEXT COMMUN
    context = {
        'rccmForm': rccmForm,
        'formaliteForm': formaliteForm,
    }

    if type_rccm == "PERSONNE PHYSIQUE":
        # Récupération des instances liées
        formalite_instance = Formalite.objects.filter(rccm=rccm_instance).last()
        personne_physique_instance = PersonnePhysique.objects.filter(formalite=formalite_instance).first()
        foyer_instance = Foyer_personne_physique.objects.filter(formalite=formalite_instance).first()
        etab_instance = EtablissementPersonne.objects.filter(formalite=formalite_instance).first()
        etab_sec_instance = EtablissementSecondairePersonne.objects.filter(formalite=formalite_instance).first()
        engage_instance = PersonnePhysiqueEngager.objects.filter(formalite=formalite_instance).first()
        gerant_instance = GerantPersonne.objects.filter(formalite=formalite_instance).first()

        # Création des formulaires
        context.update({
            'personnePhysiqueForm': PersonnePhysiqueForm(instance=personne_physique_instance),
            'foyerPersonnePhysiqueForm': FoyerPersonnePhysiqueForm(instance=foyer_instance),
            'etablissementPersonneForm': EtablissementPersonneForm(instance=etab_instance),
            'etablissementSecondaireForm': EtablissementSecondairePersonneForm(instance=etab_sec_instance),
            'personnePhysiqueEngagerForm': PersonnePhysiqueEngagerForm(instance=engage_instance),
            'gerantForm': GerantPersonneForm(instance=gerant_instance),
            'personne_engager_formset': modelformset_factory(
                PersonnePhysiqueEngager,
                form=PersonnePhysiqueEngagerForm,
                fields='__all__',
                extra=1
            )(request.POST or None, prefix='engager', queryset=PersonnePhysiqueEngager.objects.none())
        })

        return render(request, 'rccm/modification/personne_physique/form/create.html', context)

    elif type_rccm == "PERSONNE MORALE":
        personne_morale_instance = PersonneMorale.objects.filter(formalite=formalite_instance).first()
        etab_instance = EtablissementMorale.objects.filter(formalite=formalite_instance).first()
        associe_instance = AssociesMorale.objects.filter(formalite=formalite_instance).first()
        gerant_morale_instance = GerantMorale.objects.filter(formalite=formalite_instance).first()
        commissaire_instance = CommissaireComptesMorale.objects.filter(formalite=formalite_instance).first()

        context.update({
            'personneMoraleForm': PersonneMoraleForm(instance=personne_morale_instance),
            'etablissementMoraleForm': EtablissementMoraleForm(instance=etab_instance),
            'associesMoraleForm': AssociesMoraleForm(instance=associe_instance),
            'gerantMoraleForm': GerantMoraleForm(instance=gerant_morale_instance),
            'commissaireComptesMoraleForm': CommissaireComptesMoraleForm(instance=commissaire_instance),
        })

        return render(request, 'rccm/modification/personne_morale/form/create.html', context)

    else:
        return JsonResponse({"error": "Type RCCM inconnu"}, status=400)




def submit_formalite(request):
    PersonnePhysiqueEngagerFormSet = modelformset_factory(
        PersonnePhysiqueEngager,
        form=PersonnePhysiqueEngagerForm,
        fields="__all__",
        extra=0,
        can_delete=True
    )

    if request.method == 'POST':
        type_rccm = request.POST.get("typeRccm")
        formalite_form = FormaliteForm(request.POST)
        rccm_form = RccmForm(request.POST)
        chef_greffe = Account.objects.filter(groups__name="Chef").latest('id')

        # Initialisation des formulaires spécifiques selon le type RCCM
        if type_rccm == "PERSONNE PHYSIQUE":
            personne_physique_form = PersonnePhysiqueForm(request.POST)
            etablissement_form = EtablissementPersonneForm(request.POST)
            personne_engager_formset = PersonnePhysiqueEngagerFormSet(request.POST, prefix='engager')
            specific_forms = [personne_physique_form, etablissement_form]
            formset = personne_engager_formset
        elif type_rccm == "PERSONNE MORALE":
            personne_morale_form = PersonneMoraleForm(request.POST)
            etablissement_morale_form = EtablissementMoraleForm(request.POST)
            associe_form = AssociesMoraleForm(request.POST)
            gerant_form = GerantMoraleForm(request.POST)
            commissaire_form = CommissaireComptesMoraleForm(request.POST)
            specific_forms = [
                personne_morale_form,
                etablissement_morale_form,
                associe_form,
                gerant_form,
                commissaire_form
            ]
            formset = None
        else:
            return JsonResponse({"error": "Type RCCM invalide."}, status=400)

        # Validation
        all_valid = formalite_form.is_valid() and rccm_form.is_valid() and all(f.is_valid() for f in specific_forms)
        if formset:
            all_valid = all_valid and formset.is_valid()

        if all_valid:
            numero_rccm = rccm_form.cleaned_data.get('numeroRccm')
            rccm = Rccm.objects.filter(numeroRccm=numero_rccm).first()

            formalite = formalite_form.save(commit=False)
            formalite.rccm = rccm
            formalite.chef_greffe = chef_greffe
            formalite.created_by = request.user
            if not formalite_form.cleaned_data.get('typeFormalite'):
                formalite.typeFormalite = 'Création'
            formalite.save()

            formalite.declarationModificative.set(request.POST.getlist('declarationModificative'))
            formalite.optionDeclaration.set(request.POST.getlist('optionDeclaration'))

            # Traitement selon le type RCCM
            if type_rccm == "PERSONNE PHYSIQUE":
                personne_physique = personne_physique_form.save(commit=False)
                personne_physique.formalite = formalite
                personne_physique.save()

                etablissement = etablissement_form.save(commit=False)
                etablissement.formalite = formalite
                etablissement.activites = etablissement_form.cleaned_data.get('activitesActualiser') or etablissement_form.cleaned_data.get('activites')
                etablissement.save()

                for form in formset:
                    instance = form.save(commit=False)
                    instance.formalite = formalite
                    instance.save()

            elif type_rccm == "PERSONNE MORALE":
                pers_morale = personne_morale_form.save(commit=False)
                pers_morale.formalite = formalite
                pers_morale.save()

                etab_morale = etablissement_morale_form.save(commit=False)
                etab_morale.formalite = formalite
                etab_morale.save()

                associe = associe_form.save(commit=False)
                associe.formalite = formalite
                associe.save()

                gerant = gerant_form.save(commit=False)
                gerant.formalite = formalite
                gerant.save()

                commissaire = commissaire_form.save(commit=False)
                commissaire.formalite = formalite
                commissaire.save()

            # 🔔 Notification
            message = f"Une nouvelle formalité a été soumise par {request.user}."
            url = request.build_absolute_uri(reverse('rccm.formalite.detail', args=[formalite.slug]))

            destinataires = Account.objects.filter(groups__name__in=['Chef', 'Greffier']).distinct()
            for user in destinataires:
                Notification.objects.create(
                    recipient=user,
                    sender=request.user,
                    type='info',
                    message=strip_tags(message),
                    objet_cible=formalite.pk,
                    url=url
                )

            context = last_formalite()
            return render(request, 'rccm/modification/create-succes.html', context)

        else:
            errors = {
                "formalite_form": formalite_form.errors,
                "rccm_form": rccm_form.errors,
            }
            for i, form in enumerate(specific_forms):
                errors[f"specific_form_{i}"] = form.errors
            if formset:
                errors["formset"] = [form.errors for form in formset]

            return JsonResponse({"success": False, "errors": errors}, status=400)

    context = last_formalite()
    return render(request, 'rccm/modification/create-succes.html', context)



def update_formalite(request, pk):
    formalite_instance = Formalite.objects.filter(id=pk).first()
    if not formalite_instance:
        raise Http404("Formalité introuvable")

    personne_physique_instance = PersonnePhysique.objects.filter(formalite=formalite_instance).first()
    etablissement_instance = EtablissementPersonne.objects.filter(formalite=formalite_instance).first()
    rccm_instance = Rccm.objects.filter(id=formalite_instance.rccm_id).first()

    PersonnePhysiqueEngagerFormSet = modelformset_factory(
        PersonnePhysiqueEngager,
        form=PersonnePhysiqueEngagerForm,
        fields="__all__",
        extra=0,
        can_delete=True
    )

    if request.method == 'POST':
        formalite_form = FormaliteForm(request.POST, instance=formalite_instance)
        rccm_form = RccmForm(request.POST, instance=rccm_instance)
        personne_physique_form = PersonnePhysiqueForm(request.POST, instance=personne_physique_instance)
        etablissement_form = EtablissementPersonneForm(request.POST, instance=etablissement_instance)
        personne_engager_formset = PersonnePhysiqueEngagerFormSet(
            request.POST,
            queryset=PersonnePhysiqueEngager.objects.filter(formalite=formalite_instance),
            prefix='engager'
        )

        if all([
            formalite_form.is_valid(),
            rccm_form.is_valid(),
            personne_physique_form.is_valid(),
            etablissement_form.is_valid(),
        ]):
            rccm = rccm_form.save()

            formalite = formalite_form.save(commit=False)
            formalite.rccm = rccm
            formalite.save()

            # M2M fields
            formalite.declarationModificative.set(request.POST.getlist('declarationModificative'))
            formalite.optionDeclaration.set(request.POST.getlist('optionDeclaration'))

            personne_physique = personne_physique_form.save(commit=False)
            personne_physique.formalite = formalite
            personne_physique.save()

            etablissement = etablissement_form.save(commit=False)
            etablissement.formalite = formalite
            etablissement.activites = etablissement_form.cleaned_data.get('activitesActualiser') or etablissement_form.cleaned_data.get('activites')
            etablissement.save()

            if personne_engager_formset.is_valid():
                # Mise à jour des personnes engagées
                for form in personne_engager_formset:

                    if not form.has_changed():
                        continue  # Formulaire vide, ignorer

                    if form.cleaned_data.get('DELETE'):
                        if form.instance.pk:
                            form.instance.delete()
                    else:
                        instance = form.save(commit=False)
                        instance.formalite = formalite
                        instance.save()
            else:
                # Tu peux afficher les erreurs ou les enregistrer pour débogage
                print(personne_engager_formset.errors)
                errors = {
                    "personne_engager_formset": personne_engager_formset.errors,
                   
                }
                return JsonResponse({"success": False, "errors": errors}, status=400)

            return render(request, 'rccm/modification/update-succes.html', {
                'formalite': formalite
            })

        else:
            errors = {
                "formalite_form": formalite_form.errors,
                "rccm_form": rccm_form.errors,
                "personne_physique_form": personne_physique_form.errors,
                "etablissement_form": etablissement_form.errors,
            }
            return JsonResponse({"success": False, "errors": errors}, status=400)

    else:
        formalite_form = FormaliteForm(instance=formalite_instance)
        rccm_form = RccmForm(instance=rccm_instance)
        personne_physique_form = PersonnePhysiqueForm(instance=personne_physique_instance)
        etablissement_form = EtablissementPersonneForm(instance=etablissement_instance)
        personne_engager_formset = PersonnePhysiqueEngagerFormSet(
            queryset=PersonnePhysiqueEngager.objects.filter(formalite=formalite_instance),
            prefix='engager'
        )

    return render(request, 'rccm/modification/update.html', {
        'formaliteForm': formalite_form,
        'rccmForm': rccm_form,
        'personnePhysiqueForm': personne_physique_form,
        'etablissementPersonneForm': etablissement_form,
        'personne_engager_formset': personne_engager_formset,
        'formalite_id': formalite_instance.id,
    })


   
def last_formalite():
     # Gestion de la récupération des dernières données si la requête n'est pas une POST
    latest_formalite = Formalite.objects.order_by('-id').first()
    etablissement = EtablissementPersonne.objects.filter(formalite=latest_formalite).order_by('-created_at').first()
    personne_physique = PersonnePhysique.objects.filter(formalite=latest_formalite).order_by('-created_at').first()
    personne_engager = PersonnePhysiqueEngager.objects.filter(formalite=latest_formalite).order_by('-created_at').first()

    context = {
        'formalite': latest_formalite,
        'etablissement': etablissement,
        'personne_physique': personne_physique,
        'personne_engager': personne_engager,
    }

    return context




def submit_rccm(request):
    if request.method == 'POST':
        type_rccm = request.POST.get("rccm-typeRccm")  # avec le prefix 'rccm'

        # Initialisation des formulaires avec les bons prefix
        rccm_form = RccmForm(request.POST, request.FILES, prefix='rccm')
        formalite_form = FormaliteForm(request.POST, prefix='ff')

        if type_rccm == "PERSONNE PHYSIQUE":
            personne_physique_form = PersonnePhysiqueForm(request.POST, prefix='pp')
            etablissement_form = EtablissementPersonneForm(request.POST, prefix='etab')
            personne_engager_form = PersonnePhysiqueEngagerForm(request.POST, prefix='ppe')
            activite_form = ActivitesAnterieuresPersonneForm(request.POST, prefix='act')

            other_forms = [
                personne_physique_form, etablissement_form,
                personne_engager_form, activite_form
            ]

        elif type_rccm == "PERSONNE MORALE":
            personne_morale_form = PersonneMoraleForm(request.POST, prefix='pm')
            etablissement_morale_form = EtablissementMoraleForm(request.POST, prefix='etabm')
            etablissement_secondaire_morale_form = EtablissementSecondaireMoraleForm(request.POST, prefix='etabsm')
            associes_form = AssociesMoraleForm(request.POST, prefix='assoc')
            gerant_form = GerantMoraleForm(request.POST, prefix='gerantm')
            commissaire_form = CommissaireComptesMoraleForm(request.POST, prefix='ccm')

            other_forms = [
                personne_morale_form, etablissement_morale_form,etablissement_secondaire_morale_form,
                associes_form, gerant_form, commissaire_form
            ]

        else:
            return JsonResponse({"error": "Type RCCM invalide."}, status=400)

        # Validation de tous les formulaires
        if all(form.is_valid() for form in [formalite_form, rccm_form] + other_forms):
            numero_rccm = rccm_form.cleaned_data.get("numeroRccm")
            rccm = Rccm.objects.filter(numeroRccm=numero_rccm).first()

            if rccm:
                return render(request, "rccm/creation/create-error.html")

            # Création de l’objet RCCM
            rccm = rccm_form.save(commit=False)
            rccm.created_by = request.user
            if 'rccm-rccm_file' in request.FILES:
                rccm.rccm_file = request.FILES['rccm-rccm_file']
            rccm.save()

            # Formalité associée
            formalite = formalite_form.save(commit=False)
            formalite.rccm = rccm
            formalite.typeRccm = type_rccm
            formalite.dateModification = rccm.dateEnreg
            formalite.created_by = request.user
            if not formalite.typeFormalite:
                formalite.typeFormalite = "Création"
            formalite.save()

            if type_rccm == "PERSONNE PHYSIQUE":
                personne = personne_physique_form.save(commit=False)
                personne.formalite = formalite
                personne.save()

                etab = etablissement_form.save(commit=False)
                etab.formalite = formalite
                etab.save()

                engage = personne_engager_form.save(commit=False)
                engage.formalite = formalite
                engage.save()

                activite = activite_form.save(commit=False)
                activite.formalite = formalite
                activite.save()

            elif type_rccm == "PERSONNE MORALE":
                personne = personne_morale_form.save(commit=False)
                personne.formalite = formalite
                personne.save()

                etab = etablissement_morale_form.save(commit=False)
                etab.formalite = formalite
                etab.save()

                etab_second = etablissement_secondaire_morale_form.save(commit=False)
                etab_second.formalite = formalite
                etab_second.save()

                associe = associes_form.save(commit=False)
                associe.formalite = formalite
                associe.save()

                gerant = gerant_form.save(commit=False)
                gerant.formalite = formalite
                gerant.save()

                commissaire = commissaire_form.save(commit=False)
                commissaire.formalite = formalite
                commissaire.save()

            # Notifications
            message = f"Un nouveau RCCM a été enregistré par {request.user}."
            url = request.build_absolute_uri(reverse('rccm.detail', args=[formalite.id]))
            destinataires = Account.objects.filter(groups__name__in=['Chef', 'Greffier']).distinct()

            for user in destinataires:
                Notification.objects.create(
                    recipient=user,
                    sender=request.user,
                    type='info',
                    message=strip_tags(message),
                    objet_cible=formalite.pk,
                    url=url
                )

            return render(request, "rccm/creation/create-succes.html")

        else:
            # Retourner les erreurs
            errors = {
                "formalite_form": formalite_form.errors,
                "rccm_form": rccm_form.errors,
            }
            for i, form in enumerate(other_forms):
                errors[f"form_{i}"] = form.errors

            return JsonResponse({"Erreur": False, "errors": errors}, safe=False, status=400)

    return redirect('rccm.list')



def create_rccm(request):

    context = {
       'rccmForm': RccmForm(prefix='rccm'),
       'formaliteForm': FormaliteForm(prefix='ff'),
       'personnePhysiqueForm': PersonnePhysiqueForm(prefix='pp'),
       'etablissementPersonneForm': EtablissementPersonneForm(prefix='etab'),
       'personnePhysiqueEngagerForm': PersonnePhysiqueEngagerForm(prefix='ppe'),
       'activitesAnterieuresPersonneForm': ActivitesAnterieuresPersonneForm(prefix='act'),

       'personneMoraleForm': PersonneMoraleForm(prefix='pm'),
       'etablissementMoraleForm': EtablissementMoraleForm(prefix='etabm'),
       'associesMoraleForm': AssociesMoraleForm(prefix='assoc'),
       'gerantMoraleForm': GerantMoraleForm(prefix='gerantm'),
       'commissaireComptesMoraleForm': CommissaireComptesMoraleForm(prefix='ccm'),
       'etablissementSecondaireMoraleForm': EtablissementSecondaireMoraleForm(prefix='etabsm'),
    }


    return render(request, 'rccm/creation/create-rccm.html', context)



# def upload_pdf_view(request):
#     if request.method == 'POST':
#         form_file = PDFUploadForm(request.POST, request.FILES)
#         if form_file.is_valid():
#             uploaded_file = request.FILES['pdf_file']
#             type_rccm = form_file.cleaned_data.get('type_rccm')
#             request.session['uploaded_pdf'] = uploaded_file.name

#             temp_file_path = f'/tmp/{uploaded_file.name}'
#             with open(temp_file_path, 'wb+') as temp_file:
#                 for chunk in uploaded_file.chunks():
#                     temp_file.write(chunk)
#             request.session['temp_file_path'] = temp_file_path

#             extracted_text = ""
#             image_path = default_storage.save("uploads/" + uploaded_file.name, uploaded_file)
#             file_path = os.path.join(settings.MEDIA_ROOT, image_path)

#             if uploaded_file.name.endswith(".pdf"):
#                 images = convert_from_path(file_path)
#                 text_list = [pytesseract.image_to_string(img, lang="eng+fra") for img in images]
#                 extracted_text = "\n\n".join(text_list)
#             else:
#                 image = Image.open(file_path)
#                 extracted_text = pytesseract.image_to_string(image, lang="eng+fra")

#             locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')

#             num_rccm = re.search(r"N\u00b0ENTREPRISE/RCCM/(.*)", extracted_text, re.IGNORECASE)
#             num_formalite = re.search(r"N\u00b0FORMALITE/RCCM/(.*)", extracted_text, re.IGNORECASE)

#             nom_commercial = re.search(r"NOM\s+COMMERCIAL.*?:\s*(.*)", extracted_text, re.IGNORECASE)
#             sigle = re.search(r"SIGLE.*?:\s*(.*)", extracted_text, re.IGNORECASE)
#             siegeSocial = re.search(r"\(g\u00e9ographique\s+et\s+postale\).*?:\s*(.*)", extracted_text, re.IGNORECASE)
#             activites_match = re.search(r"ACTIVITE.*?:\s*(.*(?:\n.*)?)", extracted_text, re.IGNORECASE)
#             activites = "\n".join(activites_match.group(1).split("\n")[:2]) if activites_match else ''

#             date_rccm_str = re.search(r"DATE\s*:\s*(\d{1,2}\s+[A-Z\u00c9\u00c8\u00c0\u00ca\u00ce\u00d4\u00db\u00c2]+)\s+(\d{4})", extracted_text)
#             date_rccm = datetime.datetime.strptime(f"{date_rccm_str.group(1)} {date_rccm_str.group(2)}", "%d %B %Y").date() if date_rccm_str else None

#             RccmForm_data = {
#                 'numeroRccm': num_rccm.group(1).strip() if num_rccm else None,
#                 'dateEnreg': date_rccm,
#             }

#             FormaliteForm_data = {
#                 'numeroFormalite': num_formalite.group(1).strip() if num_formalite else None,
#                 'typeRccm': type_rccm,
#             }

#             EtablissementForm_data = {
#                 'sigle': sigle.group(1).strip() if sigle else '',
#                 'nomCommercial': nom_commercial.group(1).strip() if nom_commercial else '',
#                 'siegeSocial': siegeSocial.group(1).strip() if siegeSocial else '',
#                 'activites': activites,
#             }

#             if type_rccm == "PERSONNE PHYSIQUE":
#                 personne_data = extract_physique_data(extracted_text, type_rccm)
#                 pre_filled_PersonneForm = PersonnePhysiqueForm(initial=personne_data)
#                 pre_filled_EtablissementForm = EtablissementPersonneForm(initial=EtablissementForm_data)
#                 personneEngagerForm = PersonnePhysiqueEngagerForm()
#                 activitesForm = ActivitesAnterieuresPersonneForm()

#                 context = {
#                     'personnePhysiqueForm': pre_filled_PersonneForm,
#                     'etablissementPersonneForm': pre_filled_EtablissementForm,
#                     'personnePhysiqueEngagerForm': personneEngagerForm,
#                     'activitesAnterieuresPersonneForm': activitesForm,
#                 }
#             else:
#                 personne_data = extract_morale_data(extracted_text, type_rccm)
#                 pre_filled_PersonneForm = PersonneMoraleForm(initial=personne_data)
#                 pre_filled_EtablissementForm = EtablissementMoraleForm(initial=EtablissementForm_data)
#                 associesForm = AssociesMoraleForm()
#                 gerantForm = GerantMoraleForm()
#                 commissaireForm = CommissaireComptesMoraleForm()

#                 context = {
#                     'personneMoraleForm': pre_filled_PersonneForm,
#                     'etablissementMoraleForm': pre_filled_EtablissementForm,
#                     'associesMoraleForm': associesForm,
#                     'gerantMoraleForm': gerantForm,
#                     'commissaireComptesMoraleForm': commissaireForm,
#                 }

#             context.update({
#                 'rccmForm': RccmForm(initial=RccmForm_data),
#                 'formaliteForm': FormaliteForm(initial=FormaliteForm_data),
#                 'form_file': form_file,
#                 'type_rccm': type_rccm,
#                 'clignoter': True,
#             })

#             return render(request, 'rccm/creation/create-rccm.html', context)

#     return render(request, 'rccm/creation/create-rccm.html', {
#         'form_file': PDFUploadForm(),
#         'rccmForm': RccmForm(),
#         'formaliteForm': FormaliteForm(),
#         'personnePhysiqueForm': PersonnePhysiqueForm(),
#         'personneMoraleForm': PersonneMoraleForm(),
#         'etablissementPersonneForm': EtablissementPersonneForm(),
#         'etablissementMoraleForm': EtablissementMoraleForm(),
#         'etablissementSecondaireForm': EtablissementSecondairePersonneForm(),
#         'etablissementSecondaireMoraleForm': EtablissementSecondaireMoraleForm(),
#         'foyerPersonnePhysiqueForm': FoyerPersonnePhysiqueForm(),
#         'personnePhysiqueEngagerForm': PersonnePhysiqueEngagerForm(),
#         'associesMoraleForm': AssociesMoraleForm(),
#         'gerantForm': GerantPersonneForm(),
#         'gerantMoraleForm': GerantMoraleForm(),
#         'commissaireComptesMoraleForm': CommissaireComptesMoraleForm(),
#         'activitesAnterieuresPersonneForm': ActivitesAnterieuresPersonneForm(),
#     })

def extract_physique_data(text, type_rccm):
    # Expression régulière pour chaque champ pertinent
    num_rccm = re.search(r"N°ENTREPRISE/RCCM/(.*)", text, re.IGNORECASE)
    num_formalite = re.search(r"N°FORMALITE/RCCM/(.*)", text, re.IGNORECASE)
    nom = re.search(r"Mlle|Mme|M\s+(.*?)\s+PRENOM\(s\)", text, re.IGNORECASE)
    prenom = re.search(r"PRENOM\(s\)\s+:(.*)", text, re.IGNORECASE)
    lieu_naissance = re.search(r"à\s+(.*?)\s+NATIONALITE", text, re.IGNORECASE)
    nationnalite = re.search(r"NATIONALITE\s+:(.+)", text, re.IGNORECASE)
    tel = re.search(r"TÉLÉPHONE|TEL\s*:\s*(.+)", text, re.IGNORECASE)
    date_naissance_str = re.search(r"DATE\s+ET\s+LIEU\s+DE\s+NAISSANCE\s+:\s*(\d{2}-\d{2}-\d{4})", text, re.IGNORECASE)
    domicile = re.search(r"DOMICILE\s+PERSONNEL\s+:(.*)", text, re.IGNORECASE)
    siege_social = re.search(r"\(géographique\s+et\s+postale\)\s+:(.*)", text, re.IGNORECASE)
    activites_match = re.search(r"ACTIVITÉS?\s+EXERCÉES?.*?:\s*(.*(?:\n.*)?)", text, re.IGNORECASE)
    
    # Format date naissance
    date_naissance = None
    if date_naissance_str:
        try:
            date_naissance = datetime.datetime.strptime(date_naissance_str.group(1), "%d-%m-%Y").date()
        except Exception:
            date_naissance = None

    return {
        "rccm": {
            "numeroRccm": num_rccm.group(1).strip() if num_rccm else '',
            "dateEnreg": None  # Peut être dispositif plus haut ou traité ailleurs
        },
        "formalite": {
            "numeroFormalite": num_formalite.group(1).strip() if num_formalite else '',
            "typeRccm": type_rccm
        },
        "personne_physique": {
            "nom": nom.group(1).strip() if nom else '',
            "prenom": prenom.group(1).strip() if prenom else '',
            "lieuNaissance": lieu_naissance.group(1).strip() if lieu_naissance else '',
            "nationnalite": nationnalite.group(1).strip() if nationnalite else '',
            "telephone": tel.group(1).strip() if tel else '',
            "domicile": domicile.group(1).strip() if domicile else '',
            "dateNaissance": date_naissance,
        },
        "etablissement": {
            "siegeSocial": siege_social.group(1).strip() if siege_social else '',
            "activites": activites_match.group(1).strip() if activites_match else '',
        }
    }

def extract_morale_data(text, type_rccm):
    num_rccm = re.search(r"N°ENTREPRISE/RCCM/(.*)", text, re.IGNORECASE)
    num_formalite = re.search(r"N°FORMALITE/RCCM/(.*)", text, re.IGNORECASE)
    denomination = re.search(r"DÉNOMINATION\s+:\s*(.*)", text, re.IGNORECASE)
    sigle = re.search(r"SIGLE\s+OU\s+ENSEIGNE\s+:\s*(.*)", text, re.IGNORECASE)
    siege_social = re.search(r"\(géographique\s+et\s+postale\)\s+:(.*)", text, re.IGNORECASE)
    activites_match = re.search(r"ACTIVITÉS?\s+EXERCÉES?.*?:\s*(.*(?:\n.*)?)", text, re.IGNORECASE)
    capital = re.search(r"CAPITAL\s+SOCIAL\s+:\s*(.*)", text, re.IGNORECASE)
    duree = re.search(r"DURÉE\s+DE\s+LA\s+SOCIÉTÉ\s+:\s*(\d+)", text, re.IGNORECASE)

    return {
        "rccm": {
            "numeroRccm": num_rccm.group(1).strip() if num_rccm else '',
            "dateEnreg": None
        },
        "formalite": {
            "numeroFormalite": num_formalite.group(1).strip() if num_formalite else '',
            "typeRccm": type_rccm
        },
        "personne_morale": {
            "denomination": denomination.group(1).strip() if denomination else '',
            "sigle": sigle.group(1).strip() if sigle else '',
        },
        "etablissement": {
            "siegeSocial": siege_social.group(1).strip() if siege_social else '',
            "activites": activites_match.group(1).strip() if activites_match else '',
        },
        "infos_societe": {
            "capital_social": capital.group(1).strip() if capital else '',
            "duree": duree.group(1).strip() if duree else '',
        }
    }


def scan(request):

    form_file = PDFUploadForm()
    context = {
    'form_file':form_file,
    }

    return render(request, 'rccm/creation/scan.html', context)


def scanFormalite(request, slug):
    # Récupérer l'objet Formalite correspondant au slug
    formalite_signer = PDFUploadSignature()
    formalite = get_object_or_404(Formalite, slug=slug)

    if request.method == "POST":
        uploaded_file = request.FILES.get('formaliteSignee')

        
        if uploaded_file:
            # Générer un nom de fichier unique
            file_name = f"{slugify(slug)}_{uploaded_file.name}"
            file_path = f"formalites_signees/{file_name}"

            # Sauvegarder le fichier
            saved_path = default_storage.save(file_path, uploaded_file)

            if formalite.formaliteSignee:
                # Obtenir le chemin absolu du fichier existant
                existing_file_path = formalite.formaliteSignee.path

                # Vérifier si le fichier existe avant de le supprimer
                if os.path.exists(existing_file_path):
                    os.remove(existing_file_path)

            # Mettre à jour le champ et enregistrer
            formalite.formaliteSignee = saved_path
            formalite.save()

            messages.success(request, "La formalité a été signée avec succès.")
            return redirect('rccm.formalite.detail', slug=slug)

    context = {
        'formalite_signer': formalite_signer,
        'formalite_slug': slug,
    }

    return render(request, 'rccm/modification/scanSigner.html', context)


def signFormalite(request):
    password = request.POST.get('password')
    id_formalite = request.POST.get('formalite')

    formalite_instance = get_object_or_404(Formalite, id=id_formalite)

    if check_password(password, formalite_instance.chef_greffe.password):
        formalite_instance.statut = "SIGNER"
        formalite_instance.save(update_fields=['statut'])

         # 🔔 Créer la notification
        message = f"Une formalité rccm a été signée par {request.user}."
        url = request.build_absolute_uri(reverse('rccm.formalite.detail', args=[formalite_instance.slug]))
        
        roles = ['Chef', 'Greffier']
        destinataires = Account.objects.filter(groups__name__in=roles).distinct()

        for user in destinataires:
            Notification.objects.create(
                recipient=user,
                sender=request.user,
                type='info',
                message=strip_tags(message),
                objet_cible=formalite_instance.pk,
                url=url
            )

        messages.success(request, "Félicitation, la formalité a été signée avec succès !")
    else:
        messages.error(request, "Désolé, vous avez saisi un mot de passe incorrect !")

    return redirect('rccm.formalite.detail', slug=formalite_instance.slug)

def deleteFormalite(request):
    if request.method == 'POST':
        id_formalite = request.POST.get('formalite')

        try:
            formalite = Formalite.objects.get(id=id_formalite)
            formalite.delete()

            messages.success(request, "Félicitation, la formalité a été supprimée avec succès !")
            return redirect('rccm.modification')
        
        except Formalite.DoesNotExist:
            return JsonResponse({"success": False, "message": "Formalité introuvable."}, status=404)

    return JsonResponse({"success": False, "message": "Requête invalide."}, status=400)


def get_options_by_declaration(request):
    declaration_ids = request.GET.getlist('ids')
    options = OptionDeclaration.objects.filter(declaration__id__in=declaration_ids).values('id', 'label')
    return JsonResponse(list(options), safe=False)


def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="formalites.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Formalités')

    row_num = 0
    columns = ['Numéro', 'Date de création', 'Catégorie', 'Créé par', 'Type société']

    for col_num, column_title in enumerate(columns):
        ws.write(row_num, col_num, column_title)

    formalites = Formalite.objects.all()

    for f in formalites:
        row_num += 1
        ws.write(row_num, 0, f.numeroFormalite)
        ws.write(row_num, 1, str(f.dateModification))
        ws.write(row_num, 2, f.typeFormalite)
        ws.write(row_num, 3, str(f.created_by))
        ws.write(row_num, 4, str(f.typeRccm))

    wb.save(response)
    return response


def marquer_notification_lue(request, url):
    
    notifications = Notification.objects.filter(url=url, recipient=request.user)
    
    if not notifications.exists():
        pass

    notifications.update(is_read=True)

    return JsonResponse({'status': 'success', 'message': 'Notifications marquées comme lues.'})
    
