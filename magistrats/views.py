from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render,redirect
from _base.models import Juridictions
from .forms import PresidentForm,ConseillerForm,AssesseurForm
from .models import Presidents,Conseillers,Assesseurs

# Fonction presidents
def president(request, idPresident=None):

    # Si idPresident est fourni, c'est une mise à jour, sinon, c'est une création
    president = get_object_or_404(Presidents, pk=idPresident) if idPresident else None

    form = PresidentForm(request.POST or None, instance=president)
    juridictions = Juridictions.objects.all()
    presidents = Presidents.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            juridiction_id = request.POST.get('juridiction_id')
            juridiction = Juridictions.objects.get(pk=juridiction_id)

            if president:  # Si c'est une mise à jour
                president.juridiction = juridiction
                president.save()
                messages.success(request, 'Président(e) mis(e) à jour avec succès !')
            else:  # Si c'est une création
                form.save(commit=False)  # Ne pas sauvegarder immédiatement pour pouvoir modifier d'autres champs
                form.instance.juridiction = juridiction
                form.save()
                messages.success(request, 'Président(e) enregistré(e) avec succès !')

            return redirect('magistrats.president')

    context = {
        'juridictions': juridictions,
        'form': form,
        'presidents': presidents,
    }

    return render(request, 'magistrats/presidents.html', context)

def fetchPresident(request, idPresident):

    president = Presidents.objects.filter(id=idPresident).first()

    if president:
        # Convert the Juridictions object to a dictionary
        juridiction_data = {
            'idJuridiction': president.juridiction.id,
            'nomJuridiction': president.juridiction.name,
            # Add other fields of Juridictions as needed
        }

        # Build the data for the president
        data = {
            'idPresident': president.id,
            'name': president.prenomNom,
            'chambre': president.chambre,
            'juridiction': juridiction_data,  # Use the converted dictionary here
        }

        return JsonResponse(data)
    else:
        # If no president with the specified ID is found
        data = {'error': 'No president found with this ID'}
        return JsonResponse(data, status=404)

def deletePresident(request, idPresident):
    president = get_object_or_404(Presidents, pk=idPresident)
    
    if request.method == 'POST':
        president.delete()
        messages.success(request, 'Président(e) supprimé(e) avec succès !')
        return redirect('magistrats.president')
    

# Fonction conseillers
def conseiller(request, idConseiller=None):

    # Si idConseiller est fourni, c'est une mise à jour, sinon, c'est une création
    conseiller = get_object_or_404(Conseillers, pk=idConseiller) if idConseiller else None

    form = ConseillerForm(request.POST or None, instance=conseiller)
    juridictions = Juridictions.objects.all()
    conseillers = Conseillers.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            juridiction_id = request.POST.get('juridiction_id')
            juridiction = Juridictions.objects.get(pk=juridiction_id)

            if conseiller:  # Si c'est une mise à jour
                conseiller.juridiction = juridiction
                conseiller.save()
                messages.success(request, 'Conseiller(ère) mis(e) à jour avec succès !')
            else:  # Si c'est une création
                form.save(commit=False)  # Ne pas sauvegarder immédiatement pour pouvoir modifier d'autres champs
                form.instance.juridiction = juridiction
                form.save()
                messages.success(request, 'Conseiller(ère) enregistré(e) avec succès !')

            return redirect('magistrats.conseiller')

    context = {
        'juridictions': juridictions,
        'form': form,
        'conseillers': conseillers,
    }

    return render(request, 'magistrats/conseillers.html', context)

def fetchConseiller(request, idConseiller):

    conseiller = Conseillers.objects.filter(id=idConseiller).first()

    if conseiller:
        # Convert the Juridictions object to a dictionary
        juridiction_data = {
            'idJuridiction': conseiller.juridiction.id,
            'nomJuridiction': conseiller.juridiction.name,
            # Add other fields of Juridictions as needed
        }

        # Build the data for the conseiller
        data = {
            'idConseiller': conseiller.id,
            'name': conseiller.prenomNom,
            'juridiction': juridiction_data,  # Use the converted dictionary here
        }

        return JsonResponse(data)
    else:
        # If no president with the specified ID is found
        data = {'error': 'No conseiller found with this ID'}
        return JsonResponse(data, status=404)

def deleteConseiller(request, idConseiller):
    conseiller = get_object_or_404(Conseillers, pk=idConseiller)
    
    if request.method == 'POST':
        conseiller.delete()
        messages.success(request, 'Conseiller(ère) supprimé(e) avec succès !')
        return redirect('magistrats.conseiller')



# Fonction assesseurs
def assesseur(request, idAssesseur=None):

    # Si idAssesseur est fourni, c'est une mise à jour, sinon, c'est une création
    assesseur = get_object_or_404(Assesseurs, pk=idAssesseur) if idAssesseur else None

    form = AssesseurForm(request.POST or None, instance=assesseur)
    juridictions = Juridictions.objects.all()
    assesseurs = Assesseurs.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            juridiction_id = request.POST.get('juridiction_id')
            juridiction = Juridictions.objects.get(pk=juridiction_id)

            if assesseur:  # Si c'est une mise à jour
                assesseur.juridiction = juridiction
                assesseur.save()
                messages.success(request, 'Assesseur mis à jour avec succès !')
            else:  # Si c'est une création
                form.save(commit=False)  # Ne pas sauvegarder immédiatement pour pouvoir modifier d'autres champs
                form.instance.juridiction = juridiction
                form.save()
                messages.success(request, 'Assesseur enregistré avec succès !')

            return redirect('magistrats.assesseur')

    context = {
        'juridictions': juridictions,
        'form': form,
        'assesseurs': assesseurs,
    }

    return render(request, 'magistrats/assesseurs.html', context)

def fetchAsseseur(request, idAssesseur):

    assesseur = Assesseurs.objects.filter(id=idAssesseur).first()

    if assesseur:
        # Convert the Juridictions object to a dictionary
        juridiction_data = {
            'idJuridiction': assesseur.juridiction.id,
            'nomJuridiction': assesseur.juridiction.name,
            # Add other fields of Juridictions as needed
        }

        # Build the data for the assesseur
        data = {
            'idAssesseur': assesseur.id,
            'name': assesseur.prenomNom,
            'juridiction': juridiction_data,  # Use the converted dictionary here
        }

        return JsonResponse(data)
    else:
        # If no president with the specified ID is found
        data = {'error': 'No assesseur found with this ID'}
        return JsonResponse(data, status=404)

def deleteAssesseur(request, idAssesseur):
    assesseur = get_object_or_404(Assesseurs, pk=idAssesseur)
    
    if request.method == 'POST':
        assesseur.delete()
        messages.success(request, 'Assesseur supprimé avec succès !')
        return redirect('magistrats.assesseur')