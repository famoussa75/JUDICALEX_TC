import html
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render,redirect,get_object_or_404
from _base.models import Juridictions
from magistrats.models import Presidents
from .forms import RoleForm,RoleAffaireForm,EnrollementForm,DecisionsForm,MessageForm
from django.db import IntegrityError, transaction
from django.forms import inlineformset_factory, modelformset_factory
from .models import AffaireRoles, DecisionHistory, EnrollementHistory, Roles, Enrollement, Decisions, SuivreAffaire
from datetime import datetime, timedelta, date
from django.db.models import Count, Case, When, Value, CharField, Q, F, OuterRef, Subquery
from django.utils.html import mark_safe
import re
from time import sleep
from account.models import Account, Notification
import openpyxl

from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from itertools import groupby
from operator import attrgetter

from django.db.models.functions import Coalesce
from django.db.models import IntegerField


import uuid

from role.models import AffaireRoles, Decisions, Roles, MessageDefilant
from account.models import Account
from datetime import datetime, timedelta, date
from django.db.models.functions import TruncDate
from django.db.models import Count
from django.views.decorators.http import require_http_methods



# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return backoffice(request)
        



def backoffice(request):

    current_year = date.today().year
    year = int(request.GET.get('year', current_year))

    # Générer une liste d'années de 2010 à l'année courante
    available_years = list(range(2024, current_year + 1))


    today = datetime.today().date()
    start = datetime.combine(today, datetime.min.time())
    end = datetime.combine(today, datetime.max.time())

    today_roles_fond = Roles.objects.filter(juridiction=request.user.juridiction, dateEnreg=today, typeAudience='Fond')
    today_roles_refere = Roles.objects.filter(juridiction=request.user.juridiction, dateEnreg=today, typeAudience='Refere')
    today_affaires = AffaireRoles.objects.filter(role__juridiction=request.user.juridiction, role__dateEnreg=today)

    tribunal_users = Account.objects.filter(juridiction=request.user.juridiction).count()
    visiteurs_users = Account.objects.filter(
            juridiction=request.user.juridiction,
            groups__name="Visiteur"
        ).count()

    T_roles = Roles.objects.filter(juridiction=request.user.juridiction,  dateEnreg__year=year).count()
    T_roles_today = Roles.objects.filter(juridiction=request.user.juridiction, dateEnreg=today).count()

    T_roles_fond = Roles.objects.filter(juridiction=request.user.juridiction, typeAudience='Fond',  dateEnreg__year=year).count()
    fond_pourcentage = round(T_roles_fond / T_roles * 100) if T_roles != 0 else 0

    T_roles_refere = Roles.objects.filter(juridiction=request.user.juridiction, typeAudience='Refere',  dateEnreg__year=year).count()
    refere_pourcentage = round(T_roles_refere / T_roles * 100) if T_roles != 0 else 0


    T_affaires = AffaireRoles.objects.filter(role__juridiction=request.user.juridiction,  role__dateEnreg__year=year).count()
    T_affaires_today = AffaireRoles.objects.filter(role__juridiction=request.user.juridiction, role__dateEnreg=today).count()

    T_decisions = Decisions.objects.filter(juridiction=request.user.juridiction, dateDecision__year=year).count()
    T_decisions_today = Decisions.objects.filter(juridiction=request.user.juridiction, dateDecision=today).count()

    T_affaires_sp = AffaireRoles.objects.filter(role__juridiction=request.user.juridiction, role__section='Section Présidentielle',  role__dateEnreg__year=year).count()
    president_sp = AffaireRoles.objects.filter(role__juridiction=request.user.juridiction, role__section='Section Présidentielle').last()

    T_affaires_s1 = AffaireRoles.objects.filter(role__juridiction=request.user.juridiction, role__section='Premiere-Section',  role__dateEnreg__year=year).count()
    president_s1 = AffaireRoles.objects.filter(role__juridiction=request.user.juridiction, role__section='Premiere-Section').last()

    T_affaires_s2 = AffaireRoles.objects.filter(role__juridiction=request.user.juridiction, role__section='Deuxieme-Section',  role__dateEnreg__year=year).count()
    president_s2 = AffaireRoles.objects.filter(role__juridiction=request.user.juridiction, role__section='Deuxieme-Section').last()

    T_affaires_s3 = AffaireRoles.objects.filter(role__juridiction=request.user.juridiction, role__section='Troisieme-Section',  role__dateEnreg__year=year).count()
    president_s3 = AffaireRoles.objects.filter(role__juridiction=request.user.juridiction, role__section='Troisieme-Section').last()

    T_affaires_s4 = AffaireRoles.objects.filter(role__juridiction=request.user.juridiction, role__section='Quatrieme-Section',  role__dateEnreg__year=year).count()
    president_s4 = AffaireRoles.objects.filter(role__juridiction=request.user.juridiction, role__section='Quatrieme-Section').last()

    T_affaires_s5 = AffaireRoles.objects.filter(role__juridiction=request.user.juridiction, role__section='Cinquieme-Section',  role__dateEnreg__year=year).count()
    president_s5 = AffaireRoles.objects.filter(role__juridiction=request.user.juridiction, role__section='Cinquieme-Section').last()

    # Graphes 1
    today = date.today()
    start_date = today - timedelta(days=4)

    # Tous les jours de l'intervalle (pour inclure les jours sans enregistrement)
    days = [start_date + timedelta(days=i) for i in range(5)]

    # Stats depuis la base
    raw_stats = (
        AffaireRoles.objects
        .filter(
            role__juridiction=request.user.juridiction,
            role__dateEnreg__range=(start_date, today)
        )
        .annotate(day=TruncDate('role__dateEnreg'))
        .values('day')
        .annotate(total=Count('id'))
    )


    # Dictionnaire jour => total
    stats_dict = {item['day']: item['total'] for item in raw_stats}

    # Données formatées pour le graphique
    labels = [d.strftime('%Y-%m-%d') for d in days]  # ou '%Y-%m-%d' selon ton format préféré
    data = [stats_dict.get(d, 0) for d in days]  # 0 si pas d'enregistrement ce jour-là


     # Graphes 2
    stats_decisions = (
        Decisions.objects
        .filter(
            juridiction=request.user.juridiction,
            dateDecision__year=year
        )
        .values('typeDecision')
        .annotate(total=Count('id'))
        .order_by('typeDecision')  # optionnel
    )

    # Conversion en deux listes
    decision_labels = [item['typeDecision'] for item in stats_decisions]
    decision_counts = [item['total'] for item in stats_decisions]


    messages = MessageDefilant.objects.filter(actif=True).order_by('-date_creation')


    context = {
        'today':today,
        'selected_year': year,
        'available_years': available_years,
        'today_roles_fond':today_roles_fond,
        'today_roles_refere':today_roles_refere,
        'today_affaires':today_affaires,
        'T_roles':T_roles,
        'T_roles_today':T_roles_today,
        'T_affaires':T_affaires,
        'T_affaires_today':T_affaires_today,
        'T_decisions':T_decisions,
        'T_decisions_today':T_decisions_today,
        'T_roles_fond':T_roles_fond,
        'T_roles_refere':T_roles_refere,
        'fond_pourcentage':fond_pourcentage,
        'refere_pourcentage':refere_pourcentage,
        'T_affaires_sp':T_affaires_sp,
        'president_sp':president_sp,
        'T_affaires_s1':T_affaires_s1,
        'president_s1':president_s1,
        'T_affaires_s2':T_affaires_s2,
        'president_s2':president_s2,
        'T_affaires_s3':T_affaires_s3,
        'president_s3':president_s3,
        'T_affaires_s4':T_affaires_s4,
        'president_s4':president_s4,
        'T_affaires_s5':T_affaires_s5,
        'president_s5':president_s5,
        'chart_labels': labels,
        'chart_data': data,
        'decision_labels': decision_labels,
        'decision_counts': decision_counts,
        'tribunal_users': tribunal_users,
        'visiteurs_users': visiteurs_users,
        'messages': messages,
        
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'role/partial_accueil.html', context)  # HTML partiel

    return render(request, 'role/index-backoffice.html', context)



def colorize_found(query, text):
    colored_text = re.sub(r'(' + re.escape(query) + r')', r'<span style="color:red;">\1</span>', text, flags=re.IGNORECASE)
    return mark_safe(colored_text)

def listRole(request):
    current_year = date.today().year
    year = int(request.GET.get('year', current_year))
    query = request.GET.get('q', '').strip()

    # Années disponibles
    available_years = list(range(2024, current_year + 1))

    # Base queryset selon le groupe utilisateur
    if request.user.groups.filter(name='Greffe').exists():
        roles = Roles.objects.filter(juridiction=request.user.juridiction_id, dateEnreg__year=year)
    else:
        roles = Roles.objects.filter(dateEnreg__year=year)

    # Filtrage par mot-clé (recherche)
    if query:
        roles = roles.filter(
            Q(typeAudience__icontains=query) |
            Q(section__icontains=query) |
            Q(president__icontains=query) |
            Q(greffier__icontains=query) |
            Q(dateEnreg__icontains=query)
        )

    # Pagination
    paginator = Paginator(roles, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'roles': roles,  # optionnel si tu affiches uniquement page_obj
        'page_obj': page_obj,
        'selected_year': year,
        'available_years': available_years,
        'query': query,
    }
    return render(request, 'role/gestion-roles.html', context)

def export_roles_excel(request):
    query = request.GET.get('q', '')

    roles = Roles.objects.all()
    if query:
        roles = roles.filter(
            Q(typeAudience__icontains=query) |
            Q(section__icontains=query) |
            Q(president__icontains=query) |
            Q(greffier__icontains=query) |
            Q(dateEnreg__icontains=query)
        )

    # Création du fichier Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Rôles"

    # En-têtes
    ws.append(["No", "Type d'audience", "Section", "Président(e)", "Greffier(e)", "Date d'enregistrement"])

    # Lignes
    for i, role in enumerate(roles, start=1):
        ws.append([
            i,
            role.typeAudience,
            role.section,
            role.president,
            role.greffier,
            role.dateEnreg.strftime('%Y-%m-%d') if role.dateEnreg else '',
        ])

    # Réponse
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=roles.xlsx'
    wb.save(response)
    return response

def listAffaire(request):
    current_year = date.today().year
    year = int(request.GET.get('year', current_year))
    query = request.GET.get('q', '').strip()

    # Générer la liste d'années à afficher
    available_years = list(range(2024, current_year + 1))

    affaires = AffaireRoles.objects.filter(role__dateEnreg__year=year)

    # Recherche
    if query:
        affaires = affaires.filter(
            Q(numRg__icontains=query) |
            Q(demandeurs__icontains=query) |
            Q(defendeurs__icontains=query) |
            Q(objet__icontains=query)
        )

    # Pagination
    paginator = Paginator(affaires, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'selected_year': year,
        'available_years': available_years,
        'query': query,
    }
    return render(request, 'role/gestion-affaires.html', context)

def export_affaires_excel(request):
    query = request.GET.get('q', '').strip()

    affaires = AffaireRoles.objects.all()

    if query:
        affaires = affaires.filter(
            Q(numRg__icontains=query) |
            Q(demandeurs__icontains=query) |
            Q(defendeurs__icontains=query) |
            Q(objet__icontains=query)
        )

    # Création Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Affaires"

    ws.append(["No", "RG", "Demanderesse", "Défenderesse", "Objet"])

    for i, affaire in enumerate(affaires, start=1):
        ws.append([
            i,
            affaire.numRg,
            affaire.demandeurs,
            affaire.defendeurs,
            affaire.objet,
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=affaires.xlsx'
    wb.save(response)
    return response


def listEnrollement(request):
    if request.user.groups.filter(name='Greffe').exists():
        enrollements = Enrollement.objects.filter(juridiction=request.user.juridiction_id)
        return render(request, 'role/gestion-enrollements.html',{'enrollements':enrollements})
    else:
        juridictions = Juridictions.objects.all()

        # Nombre d'objets par page
        objets_par_page = 12

        paginator = Paginator(juridictions, objets_par_page)

        # Récupérez le numéro de page à partir de la requête GET
        page_number = request.GET.get('page')
        
        # Obtenez les objets pour la page demandée
        juridictions = paginator.get_page(page_number)

        return render(request, 'role/registres-enrollements.html',{'juridictions':juridictions})



def listEnrollementForAdmin(request):
    current_year = date.today().year
    year = int(request.GET.get('year', current_year))

    query = request.GET.get('q', '')  # Récupération du mot-clé
    available_years = list(range(2024, current_year + 1))

    # Base queryset
    enrollements = Enrollement.objects.filter(
        dateEnrollement__year=year
    ).order_by('id')

    # Filtrage par recherche (parties, objet, RG, etc.)
    if query:
        enrollements = enrollements.filter(
            Q(numRg__icontains=query) |
            Q(typeAudience__icontains=query) |
            Q(section__icontains=query) |
            Q(objet__icontains=query) |
            Q(demandeurs__icontains=query) |
            Q(defendeurs__icontains=query) |
            Q(dateEnrollement__icontains=query) |
            Q(dateAudience__icontains=query) 
        )


    paginator = Paginator(enrollements, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    sections = (
            ("Premiere-Section", "Prémière Section"),
            ("Deuxieme-Section", "Deuxième Section"),
            ("Troisieme-Section", "Troisième Section"),
            ("Quatrieme-Section", "Quatrième Section"),
            ("Cinquieme-Section", "Cinquième Section"),
            ("Section-Presidentielle", "Section Présidentielle"),
    )


    return render(request, 'role/gestion-enrollements.html', {
        'page_obj': page_obj,
        'available_years': available_years,
        'selected_year': year,
        'sections': sections,
        'query': query  # pour réafficher dans le champ
    })




def export_enrollements_excel(request, idJuridiction):
    year = int(request.GET.get('year', date.today().year))
    query = request.GET.get('q', '')

    enrollements = Enrollement.objects.filter(
        juridiction=idJuridiction,
        dateEnrollement__year=year
    )

    if query:
        enrollements = enrollements.filter(
            Q(numRg__icontains=query) |
            Q(typeAudience__icontains=query) |
            Q(section__icontains=query) |
            Q(objet__icontains=query) |
            Q(demandeurs__icontains=query) |
            Q(defendeurs__icontains=query) |
            Q(dateEnrollement__icontains=query) |
            Q(dateAudience__icontains=query)
        )

    # Créer un fichier Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Enrôlements"

    # En-têtes
    ws.append([
        "No", "RG", "Type d'audience", "Section",
        "Date d'enrôlement", "Date d'audience",
        "Demanderesse", "Défenderesse", "Objet"
    ])

    # Contenu
    for i, e in enumerate(enrollements, start=1):
        ws.append([
            i,
            e.numRg,
            e.typeAudience,
            e.section,
            e.dateEnrollement.strftime('%Y-%m-%d') if e.dateEnrollement else '',
            e.dateAudience.strftime('%Y-%m-%d') if e.dateAudience else '',
            e.demandeurs,
            e.defendeurs,
            e.objet
        ])

    # Réponse HTTP avec fichier Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"enrollements_{year}.xlsx"
    response['Content-Disposition'] = f'attachment; filename={filename}'

    wb.save(response)
    return response



def export_enrollements_pdf(request, juridiction_id):
    year = request.GET.get('year')
    search = request.GET.get('q')

    enrollements = Enrollement.objects.filter(juridiction_id=juridiction_id)
    if year:
        enrollements = enrollements.filter(dateEnrollement__year=year)
    if search:
        enrollements = enrollements.filter(numAffaire__icontains=search)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="enrollements_{year or "tous"}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=landscape(A4), rightMargin=10, leftMargin=10, topMargin=20, bottomMargin=20)
    elements = []
    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    style_normal.fontSize = 8  # police réduite pour éviter débordement
    style_normal.leading = 10  # espace entre lignes dans une cellule

    # Titre
    title = Paragraph(f"REGISTRE D'ENROLLEMENTS ({year or 'Tous'})", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    # Données du tableau avec Paragraph pour wrap text
    data = [
        [
            Paragraph("NUA", styles["Heading5"]),
            Paragraph("RG", styles["Heading5"]),
            Paragraph("Date Enrôlement", styles["Heading5"]),
            Paragraph("Date Audience", styles["Heading5"]),
            Paragraph("Demanderesse", styles["Heading5"]),
            Paragraph("Défenderesse", styles["Heading5"]),
            Paragraph("Objet", styles["Heading5"])
        ]
    ]

    for e in enrollements:
        data.append([
            Paragraph(e.numAffaire or "", style_normal),
            Paragraph(e.numRg or "", style_normal),
            Paragraph(e.dateEnrollement.strftime('%d/%m/%Y') if e.dateEnrollement else '', style_normal),
            Paragraph(e.dateAudience.strftime('%d/%m/%Y') if e.dateAudience else '', style_normal),
            Paragraph(e.demandeurs or "", style_normal),
            Paragraph(e.defendeurs or "", style_normal),
            Paragraph(e.objet or "", style_normal)
        ])

    # Largeurs de colonnes adaptées
    col_widths = [60, 50, 80, 80, 130, 130, 250]

    # Création du tableau
    table = Table(data, repeatRows=1, colWidths=col_widths)

    # Style
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4CAF50')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),  # alignement en haut
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 9),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),

        ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
        ('GRID', (0,0), (-1,-1), 0.3, colors.grey),
    ]))

    elements.append(table)
    doc.build(elements)
    return response



def edit_affaire(request, idAffaire):

    enrollement = get_object_or_404(Enrollement, id=idAffaire)

    numAffaire = request.POST.get('numAffaire', '').strip()
    affaireRole = AffaireRoles.objects.filter(numAffaire=numAffaire).first()
  
    if affaireRole :

        messages.error(request, 'Modification non autorisée car cette affaire est déjà au rôle.')

    else :

        # Historique modification
        old = Enrollement.objects.get(pk=enrollement.id)
        EnrollementHistory.objects.create(
            original=old,
            numOrdre=old.numOrdre,
            numRg=old.numRg,
            numAffaire=old.numAffaire,
            objet=old.objet,
            decision=old.decision,
            demandeurs=old.demandeurs,
            defendeurs=old.defendeurs,
            dateEnrollement=old.dateEnrollement,
            dateAudience=old.dateAudience,
            juridiction=old.juridiction,
            typeAudience=old.typeAudience,
            section=old.section,
            statut=old.statut,
            motifAnnulation=old.motifAnnulation,
            modified_by=request.user
        )
          # Mise à jour dans enrollement
        enrollement.typeAudience = request.POST.get('typeAudience', '').strip()
        enrollement.dateEnrollement = request.POST.get('dateEnrollement')
        enrollement.dateAudience = request.POST.get('dateAudience')
        enrollement.demandeurs = request.POST.get('demandeurs', '').strip()
        enrollement.defendeurs = request.POST.get('defendeurs', '').strip()
        enrollement.objet = request.POST.get('objet', '').strip()
        enrollement.statut = 'Modifier'
        enrollement.save()


        messages.success(request, 'Affaire modifiée avec succès !')

    return redirect('role.enrollementForAdmin')

    

def createRole(request):
    
    juridictions = Juridictions.objects.filter(id=request.user.juridiction_id)

    form = RoleForm(request.POST or None)

    enrollFormset = modelformset_factory(Enrollement, form=EnrollementForm, extra=0, exclude=['id'])
    formset = enrollFormset(request.POST or None, queryset=Enrollement.objects.filter(juridiction_id=request.user.juridiction_id))
    
 
    if request.method == 'POST':
       
         if form.is_valid():
           
            try:
                with transaction.atomic():
                    juridiction_id = request.POST.get('juridiction_id')
                    juridiction = Juridictions.objects.get(pk=juridiction_id)
                    role = form.save(commit=False)
                    role.juridiction = juridiction
                    role.created_by = request.user
                    role.save()

                    if formset.is_valid():
                        for affaire_form2 in formset:
                            idAffairefront = affaire_form2.cleaned_data.get('idAffaire')
                            if idAffairefront is not None:
                                id_affaire = affaire_form2.cleaned_data.get('idAffaire')
                            else:
                                id_affaire = uuid.uuid4() 
                            num_ordre = affaire_form2.cleaned_data.get('numOrdre')
                            num_rg = affaire_form2.cleaned_data.get('numRg')
                            num_aff = affaire_form2.cleaned_data.get('numAffaire')
                            demandeurs = affaire_form2.cleaned_data.get('demandeurs')
                            defendeurs = affaire_form2.cleaned_data.get('defendeurs')
                            objet = affaire_form2.cleaned_data.get('objet')
                            mandatDepot = affaire_form2.cleaned_data.get('mandatDepot')
                            detention = affaire_form2.cleaned_data.get('detention')
                            prevention = affaire_form2.cleaned_data.get('prevention')
                            natureInfraction = affaire_form2.cleaned_data.get('natureInfraction')
                            decision = affaire_form2.cleaned_data.get('decision')
                            prevenus = affaire_form2.cleaned_data.get('prevenus')
                            appelants = affaire_form2.cleaned_data.get('appelants')
                            intimes = affaire_form2.cleaned_data.get('intimes')
                            partieCiviles = affaire_form2.cleaned_data.get('partieCiviles')
                            civileResponsables = affaire_form2.cleaned_data.get('civileResponsables')
                            created_by = request.user

                             # Vérifiez si toutes les variables sont None
                            if all(value is None for value in [
                                num_ordre, num_rg, num_aff, demandeurs, defendeurs, objet, mandatDepot, 
                                detention, prevention, natureInfraction, decision, prevenus, appelants, 
                                intimes, partieCiviles, civileResponsables, created_by
                            ]):
                                continue  # Passer à l'itération suivante

                            affaireEnroller = AffaireRoles(role=role,idAffaire=id_affaire,numOrdre=num_ordre,numRg=num_rg,numAffaire=num_aff,objet=objet,
                                                       mandatDepot=mandatDepot,detention=detention,prevention=prevention,natureInfraction=natureInfraction,decision=decision,
                                                       prevenus=prevenus,demandeurs=demandeurs,defendeurs=defendeurs,appelants=appelants,intimes=intimes,partieCiviles=partieCiviles,civileResponsables=civileResponsables,created_by=created_by)
                            affaireEnroller.save()

                       
                        messages.success(request, 'Rôle enregistré avec succès !')
                        return redirect('role.liste')

                        # Reste de votre code après avoir traité les valeurs du formset2
                    else:
                        print(f"Formset is not valid: {formset.errors}")
                        messages.error(request, f"Une erreur est survenu lors de la création !  {formset.errors}")
                        return redirect('role.create')

            except IntegrityError as e:
                print(f"IntegrityError occurred: {e}")
                return redirect('role.create')

   
    context = {
        'juridictions':juridictions,
        'form':form,
        'formset':formset,
    }        
    return render(request, 'role/new-role.html',context)

def valide_role(request, pk):
    role=Roles.objects.get(pk=pk)
    role.statut='Valider'
    role.save()
    messages.success(request, 'Rôle validé avec succès !')
    return redirect('role.detail', pk=role.idRole)


def createEnrollement(request):

    juridictions = Juridictions.objects.filter(id=request.user.juridiction_id)

    context = {}
    form = RoleForm(request.POST or None)
    EnrollementFormset = modelformset_factory(Enrollement, form=EnrollementForm, extra=0)
    formset = EnrollementFormset(request.POST or None, queryset=Enrollement.objects.none())

  
    if request.method == 'POST':
       
        if form.is_valid() and formset.is_valid():
           
            try:
                with transaction.atomic():
                    juridiction_id = request.POST.get('juridiction_id')
                    typeAudience = request.POST.get('typeAudience')
                    section = 'Section-Presidentielle'
                    juridiction = Juridictions.objects.get(pk=juridiction_id)
                    
                    for affaire_form in formset:
                        affaire = affaire_form.save(commit=False)
                        affaire.juridiction = juridiction
                        affaire.typeAudience = typeAudience
                        affaire.section = section
                        affaire.created_by = request.user
                         # Vérification si l'affaire existe déjà dans la BD en fonction de certains champs
                        try:
                            affaire_existe = Enrollement.objects.filter(
                                numOrdre=affaire.numOrdre, 
                                numRg=affaire.numRg, 
                                juridiction=juridiction,
                                typeAudience=typeAudience,
                                section=section,
                                dateAudience=affaire.dateAudience
                            ).exists()

                            if affaire_existe:
                                # Si l'affaire existe déjà, ne pas l'enregistrer et passer à la suivante
                                # messages.warning(request, f"L'affaire avec le numéro d'ordre {affaire.numOrdre} existe déjà et n'a pas été enregistrée.")
                                continue
                            else:
                                # Si l'affaire n'existe pas, on l'enregistre
                                affaire.save()

                                date_str = affaire.dateEnrollement.strftime("%d%m%y")
                                r_f = affaire.typeAudience
                                tribunal = 'TC'
                                if r_f == 'Refere':
                                    initial = 'R'
                                else:
                                    initial = 'F'

                                affaire.numAffaire = f"JUD{initial}{date_str}{tribunal}{affaire.id}"

                                affaire.save()  # Sauvegarde finale avec numRg mis à jour
                                
                        except Exception as e:
                            messages.error(request, f"Erreur lors de l'enregistrement de l'affaire : {e}")
                            return redirect('role.createEnrollement')
                        
                    messages.success(request, 'Affaire(s) enrollée(s) avec succès !')
                    return redirect('role.enrollementForAdmin')

            except IntegrityError as e:
                messages.error(request, f"Erreur d'intégrité : {e}")
                return redirect('role.createEnrollement')
            except Exception as e:
                messages.error(request, f"Une erreur est survenue : {e}")
                return redirect('role.createEnrollement')
        else:
            # Si form ou formset ne sont pas valides, afficher les erreurs
            if form.errors:
                messages.error(request, f"Erreurs dans le formulaire principal : {form.errors}")
            if formset.errors:
                messages.error(request, f"Erreurs dans le formset : {formset.errors}")    

   
    context = {
        'juridictions':juridictions,
        'form':form,
        'formset':formset,
    }        
    return render(request, 'role/new-enrollement.html',context)

@require_http_methods(["POST"])
def cancel_affaire(request, id):
    affaire = get_object_or_404(Enrollement, id=id)
    numAffaire = affaire.numAffaire
    affaireRole = AffaireRoles.objects.filter(numAffaire=numAffaire).first()
    if affaireRole :
         messages.error(request, 'Cette affaire est déjà au rôle !')
    else :
        affaire.statut = 'Annuler'
        affaire.motifAnnulation = request.POST.get('motifAnnulation')
        affaire.save()

        messages.success(request, 'Affaire annulée avec succès !')
    
    return redirect('role.enrollementForAdmin')  # ou autre URL de redirection

def roleDetail(request, pk):
    search_query = request.GET.get('search', '')
    role = Roles.objects.filter(idRole=pk).first()

    if not role:
        return HttpResponse("Rôle non trouvé", status=404)

    # Sous-requête : compter toutes les décisions avec le même numAffaire
    decisions_count_subquery = (
        Decisions.objects.filter(numAffaire=OuterRef('numAffaire'))
        .values('numAffaire')
        .annotate(total=Count('id'))
        .values('total')[:1]
    )

    # Annoter chaque affaire avec nb_decisions global et catégorie
    affaires = AffaireRoles.objects.filter(role=role).annotate(
        nb_decisions=Coalesce(
            Subquery(decisions_count_subquery, output_field=IntegerField()), 
            0
        ),
        categorie=Case(
            When(nb_decisions__lt=2, then=Value('Nouvelles Affaires')),
            When(nb_decisions__gte=2, then=Value('Affaires Encours')),
            output_field=CharField(),
        )
    ).order_by('categorie', 'numOrdre')

    # Recherche
    if search_query:
        affaires = affaires.filter(Q(objet__icontains=search_query))

    # Pagination unique
    paginator = Paginator(affaires, 10)  # 10 affaires par page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Grouper par catégorie pour le template
    sorted_affaires = sorted(page_obj.object_list, key=attrgetter('categorie', 'numOrdre'))
    grouped_affaires = []
    for categorie, items in groupby(sorted_affaires, key=attrgetter('categorie')):
        grouped_affaires.append({
            'grouper': categorie,
            'items': list(items)
        })

    # Infos utilisateur et juridiction
    juridiction = Juridictions.objects.filter(id=role.juridiction_id).first()
    is_chef = request.user.groups.filter(name='Chef').exists()
    affaireSuivis = SuivreAffaire.objects.filter(account=request.user) if request.user.is_authenticated else SuivreAffaire.objects.none()

    context = {
        'role': role,
        'grouped_affaires': grouped_affaires,
        'page_obj': page_obj,
        'is_chef': is_chef,
        'affaireSuivis': affaireSuivis
    }

    # Choix du template selon juridiction et type d'audience
    if juridiction and juridiction.name == 'Tribunal de Commerce de Conakry' and role.typeAudience == 'Fond':
        return render(request, 'role/details/tc-fond-detail.html', context)
    elif juridiction and juridiction.name == 'Tribunal de Commerce de Conakry' and role.typeAudience == 'Refere':
        return render(request, 'role/details/tc-refere-detail.html', context)
    else:
        return HttpResponse("Template non disponible pour cette juridiction/type d'audience")
    

def detailAffaire(request, idAffaire):


    type_section = (

        ("Premiere-Section", "Prémière Section"),
        ("Deuxieme-Section", "Deuxième Section"),
        ("Troisieme-Section", "Troisième Section"),
        ("Quatrieme-Section", "Quatrième Section"),
        ("Cinquieme-Section", "Cinquième Section"),
        ("Section-Presidentielle", "Section Présidentielle"),
    )

    type_decisions = (
        ("Renvoi", "Renvoi"),
        ("Mise-en-delibere", "Mise en délibéré"),
        ("Delibere-proroge", "Délibéré prorogé"),
        ("Vide-du-delibere", "Vidé du délibéré"),
        ("Radiation", "Radiation"),
        ("Renvoi-sine-die", "Renvoi sine die"),
        ("Affectation", "Affectation"),
    )

    affaire = AffaireRoles.objects.filter(idAffaire=idAffaire).first()
    decisions = Decisions.objects.select_related('affaire').filter(
        affaire__objet=affaire.objet,
        affaire__demandeurs=affaire.demandeurs,
        affaire__defendeurs=affaire.defendeurs,
        affaire__mandatDepot=affaire.mandatDepot,
        affaire__detention=affaire.detention,
        affaire__prevention=affaire.prevention,
        affaire__natureInfraction=affaire.natureInfraction,
        affaire__prevenus=affaire.prevenus,
        affaire__appelants=affaire.appelants,
        affaire__intimes=affaire.intimes,
        affaire__partieCiviles=affaire.partieCiviles,
        affaire__civileResponsables=affaire.civileResponsables
    )
    affaireRole = AffaireRoles.objects.select_related('role__juridiction').get(id=affaire.id)
    affaireEnroller = Enrollement.objects.filter(idAffaire=idAffaire).first()


    is_suivi = SuivreAffaire.objects.filter(affaire=affaire,juridiction=affaireRole.role.juridiction,account=request.user)
    is_greffe = request.user.groups.filter(name='Greffe').exists()
    juridiction = Juridictions.objects.filter(id=request.user.juridiction_id).first()

    if request.method == 'POST':
        form = DecisionsForm(request.POST)
        newSection = request.POST.get('section')
        juridiction_id = request.POST.get('juridiction')
        typeAudience = request.POST.get('typeAudience')

        if form.is_valid():
            decision = form.save(commit=False)
            decision.affaire = affaire
            decision.numAffaire = affaire.numAffaire
            decision.juridiction = juridiction
            decision.created_by = request.user
            decision.dateDecision = affaire.role.dateEnreg

            if newSection:
                decision.section = newSection
            else:
                decision.section = affaire.role.section
          
            form.save()



        
            messages.success(request, 'Décision ajoutée avec succès !')
            return redirect(request.META.get('HTTP_REFERER', '/'))  
    else:
        form = DecisionsForm()

    

    context = {
        'affaire':affaire,
        'affaireEnroller':affaireEnroller,
        'decisions':decisions,
        'is_greffe':is_greffe,
        'is_suivi':is_suivi,
        'type_section':type_section,
        'type_decisions': type_decisions,
        'form': form
    }

    # Formater l'URL avec l'ID dynamique
    url = f'/role/affaires/details/{idAffaire}'

    # Effectuer la mise à jour
    Notification.objects.filter(
        Q(recipient=request.user) & 
        Q(url=url) & 
        Q(is_read=False)
    ).update(is_read=True)
    return render(request, 'role/detail-affaire.html',context)
  

def fetchForm(request, selectedJuridiction, selectedType, dateRole, selectedSection):
    juridiction = Juridictions.objects.filter(id=selectedJuridiction).first()
    affaireEnrollers = Enrollement.objects.filter(
        juridiction=juridiction, typeAudience=selectedType, dateAudience=dateRole, section=selectedSection, statut='Creer'
    )
    decisionsRenvoyers = Decisions.objects.filter(
        Q(prochaineAudience=dateRole) &
        Q(juridiction=juridiction) &
        Q(affaire__role__typeAudience=selectedType) &
        Q(section=selectedSection) &
       (Q(typeDecision='Renvoi') | Q(typeDecision='Mise-en-delibere') | Q(typeDecision='Delibere-proroge') | Q(typeDecision='Affectation'))
    ).select_related('affaire')
    
    print(affaireEnrollers)
    for decision in decisionsRenvoyers:
        print("ID de la décision:", decision.idDecision)
        print("Juridiction:", decision.juridiction)
        print("Type de décision:", decision.typeDecision)
        print("Objet:", decision.objet)
        print("Président:", decision.president)
        print("Greffier:", decision.greffier)
        print("Date de la décision:", decision.dateDecision)
        print("Prochaine audience:", decision.prochaineAudience)
        print("Affaire liée:", decision.affaire)
        if decision.affaire:  # Pour afficher des détails de l'affaire liée
            print("ID de l'affaire:", decision.affaire.idAffaire)
            print("Objet de l'affaire:", decision.affaire.objet)
        print("--------")


    verifRole = Roles.objects.filter(
        juridiction=juridiction, typeAudience=selectedType, dateEnreg=dateRole, section=selectedSection
    )
    message = ''

    default_data = []

    # Vérifiez si un rôle existe déjà
    if verifRole.exists():
        message = 'Le rôle pour cette date a déjà été enregistré !'
        return render(request, 'role/roleForms/message_role_exist.html', {'message': message})
    else:

        # Ajoutez les données de `decisionsRenvoyers` à `default_data`
        for d in decisionsRenvoyers:
            default_data.append({
                'typeDecision': d.typeDecision,
                'decision': d.decision,
                'prochaineAudience': d.prochaineAudience,
                'president': d.president,
                'greffier': d.greffier,
                'dateDecision': d.dateDecision,
                'numRg': d.affaire.numRg,
                'demandeurs': d.affaire.demandeurs,
                'defendeurs': d.affaire.defendeurs,
                'numAffaire': d.affaire.numAffaire,
                'objet': d.affaire.objet,
                'idAffaire': d.affaire.idAffaire if d.affaire else None,  # Exemple d'accès à `AffaireRoles`
            })

        # Ajoutez les données d'`affaireEnrollers` à `default_data`
        for a in affaireEnrollers:
            default_data.append({
                'numOrdre': a.numOrdre,
                'idAffaire': a.idAffaire,
                'numRg': a.numRg,
                'numAffaire': a.numAffaire,
                'demandeurs': a.demandeurs,
                'defendeurs': a.defendeurs,
                'objet': a.objet,
                'dateEnrollement': a.dateEnrollement,
                'dateAudience': a.dateAudience
            })

       
        # Initialisez le formset avec `default_data`
        enrollementFormset = modelformset_factory(Enrollement, form=EnrollementForm, extra=len(default_data))
        formset = enrollementFormset(request.POST or None, queryset=Enrollement.objects.none(), initial=default_data)

    # Création du formulaire principal
    form = RoleForm(request.POST or None)

    # Contexte pour les templates
    context = {
        'formset': formset,
        'form': form,
        'message': message,
        'default_data': default_data,
        'affaireEnrollers': affaireEnrollers,
        'decisionsRenvoyers': decisionsRenvoyers,
        'selectedJuridiction': selectedJuridiction,
        'selectedType': selectedType,
        'dateRole': dateRole,
        'selectedSection': selectedSection,
    }

    # Chargement de différents templates selon `juridiction` et `selectedType`
    if juridiction.name == 'Tribunal de Commerce de Conakry' and selectedType == 'Fond':
        return render(request, 'role/roleForms/tc-fond.html', context)
    elif juridiction.name == 'Tribunal de Commerce de Conakry' and selectedType == 'Refere':
        return render(request, 'role/roleForms/tc-refere.html', context)
    else:
        return HttpResponse()


def fetchFormEnrollement(request, selectedJuridiction,selectedType):
    juridiction = Juridictions.objects.filter(id=selectedJuridiction).first()
    enrollementFormset = modelformset_factory(Enrollement, form=EnrollementForm, extra=1)
    formset = enrollementFormset(request.POST or None, queryset=Enrollement.objects.none())
    form = EnrollementForm(request.POST or None)

    context = {
        'formset':formset,
        'form':form,
    }
    if juridiction.name=='Tribunal de Commerce de Conakry' and selectedType=='Fond':
        return render(request, 'role/enrollementForms/tc-fond.html',context)
    elif juridiction.name=='Tribunal de Commerce de Conakry' and selectedType=='Refere':
        return render(request, 'role/enrollementForms/tc-refere.html',context)
    else:
        return HttpResponse()

def download_pdf(request):
    # Récupérer le contenu HTML de la requête POST
    html_content = request.POST.get('html_content', '')

    # Convertir le HTML en PDF avec weasyprint
    pdf_file = html(string=html_content).write_pdf()

    # Créer une réponse avec le PDF
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="contenu.pdf"'

    return response


def updateRole(request):

    if request.method == 'POST':
        if request.POST.get('idAffaire'):        
            idAffaire = request.POST.get('idAffaire')
            # Table affaire role
            obj = AffaireRoles.objects.filter(idAffaire=idAffaire).first()

            if request.POST.get('demandeurs'): 
                obj.demandeurs = request.POST.get('demandeurs')
            if request.POST.get('defendeurs'): 
                obj.defendeurs = request.POST.get('defendeurs')
            if request.POST.get('objet'): 
                obj.objet = request.POST.get('objet')
            if request.POST.get('decision'): 
                obj.decision = request.POST.get('decision')
        
            obj.save()

            # Table enrollement
            obj2 = Enrollement.objects.filter(idAffaire=idAffaire).first()

            if obj2 is not None:
                if request.POST.get('demandeurs'): 
                    obj2.demandeurs = request.POST.get('demandeurs')
                if request.POST.get('defendeurs'): 
                    obj2.defendeurs = request.POST.get('defendeurs')
                if request.POST.get('objet'): 
                    obj2.objet = request.POST.get('objet')
                if request.POST.get('decision'): 
                    obj2.decision = request.POST.get('decision')

                obj2.save()
            
        else:
            idRole = request.POST.get('idRole')
            obj = Roles.objects.filter(id=idRole).first()

            if request.POST.get('dateEnreg'): 
                obj.dateEnreg = request.POST.get('dateEnreg')
            if request.POST.get('president'): 
                obj.president = request.POST.get('president')
            if request.POST.get('juge'): 
                obj.juge = request.POST.get('juge')
            if request.POST.get('greffier'):
                obj.greffier = request.POST.get('greffier')
            if request.POST.get('assesseur'):
                obj.assesseur = request.POST.get('assesseur')
            if request.POST.get('assesseur1'):
                obj.assesseur1 = request.POST.get('assesseur1')
            if request.POST.get('assesseur2'):
                obj.assesseur2 = request.POST.get('assesseur2')
            if request.POST.get('conseillers'):
                obj.conseillers = request.POST.get('conseillers')
            if request.POST.get('ministerePublic'):
                obj.ministerePublic = request.POST.get('ministerePublic')
            if request.POST.get('typeAudience'):
                obj.typeAudience = request.POST.get('typeAudience')
            if request.POST.get('dateEnreg'):
                obj.dateEnreg = request.POST.get('dateEnreg')
            if request.POST.get('procureurMilitaire'):
                obj.procureurMilitaire = request.POST.get('procureurMilitaire')
            if request.POST.get('subtituts'):
                obj.subtituts = request.POST.get('subtituts')
            

            obj.save()
            
    return redirect(request.META.get('HTTP_REFERER', '/'))

def deleteRole(request):
    role = get_object_or_404(Roles, id=request.POST.get('idRole'))
    role.delete()
    messages.success(request, 'Rôle supprimé avec succès !')
    return redirect('role.liste')

def deleteDecision(request):
    decision = get_object_or_404(Decisions, id=request.POST.get('idDecision'))
    decision.delete()
    messages.success(request, 'Décision supprimée avec succès !')
    idAffaire=request.POST.get('idAffaire')
    return redirect('affaires.details' , idAffaire )

@csrf_exempt
def suivreAffaire(request):
   if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_ids = data.get('selected', [])
            account = request.user  # Assuming there is a one-to-one relationship with the user
            
            for id_affaire in selected_ids:
                is_suivi = SuivreAffaire.objects.filter(affaire_id=id_affaire,account=request.user)
                if not is_suivi :
                    affaire = AffaireRoles.objects.select_related('role__juridiction').get(id=id_affaire)
                    SuivreAffaire.objects.create(
                        affaire=affaire,
                        account=account,
                        juridiction=affaire.role.juridiction
                    )
            messages.success(request, 'Félicitation! Vous suivez désormais ces affaires.')
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
   return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@csrf_exempt
def NePasSuivreAffaire(request):
   if request.method == 'POST':
        try:
            data = json.loads(request.body)
            selected_ids = data.get('selected', [])
            #juridiction_id = data.get('juridiction_id')
            account = request.user  # Assuming there is a one-to-one relationship with the user
            
            for id_affaire in selected_ids:
                is_suivi = SuivreAffaire.objects.filter(affaire_id=id_affaire,account=account)
                if is_suivi :
                    is_suivi.delete()
                    
            messages.success(request, 'Vous ne suivez plus ces affaires.')
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
   return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
   

def update_decision(request):
    if request.method == 'POST':
        decision_id = request.POST.get('decision_id')
        decision = get_object_or_404(Decisions, id=decision_id)

        # Historique modification
        old = Decisions.objects.get(id=decision.id)
        DecisionHistory.objects.create(
            original=old,
            juridiction=old.juridiction,
            affaire=old.affaire,
            decision=old.decision,
            section=old.section,
            typeDecision=old.typeDecision,
            objet=old.objet,
            president=old.president,
            greffier=old.greffier,
            dateDecision=old.dateDecision,
            dispositif=old.dispositif,
            prochaineAudience=old.prochaineAudience,
            modified_by=request.user
        )

        # Modification decision
        decision.typeDecision = request.POST.get('typeDecision')
        decision.dateDecision = request.POST.get('dateDecision') or None
        decision.decision = request.POST.get('decision')
        decision.dateDecision = request.POST.get('dateDecision')
        decision.prochaineAudience = request.POST.get('prochaineAudience') or None
        decision.statut = 'Modifier'

        decision.save()

        messages.success(request, "Décision mise à jour avec succès.")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    messages.error(request, "Méthode non autorisée.")
    return redirect('/')


def ges_message(request, pk=None, action=None):
    messages = MessageDefilant.objects.all().order_by('-date_creation')

    # Créer ou éditer
    if pk and action == 'edit':
        instance = get_object_or_404(MessageDefilant, pk=pk)
        form = MessageForm(request.POST or None, instance=instance)
        form_title = "Modifier le message"
    else:
        instance = None
        form = MessageForm(request.POST or None)
        form_title = "Ajouter un message"

    if request.method == 'POST':
        if 'delete_id' in request.POST:
            message_to_delete = get_object_or_404(MessageDefilant, pk=request.POST['delete_id'])
            message_to_delete.delete()
            return redirect('ges_message')

        if form.is_valid():
            form.save()
            return redirect('ges_message')

    return render(request, 'role/gestion-message.html', {
        'messages': messages,
        'form': form,
        'form_title': form_title,
        'edit_mode': pk and action == 'edit',
        'instance_id': instance.pk if instance else None,
    })


def historique_modifications_enrollement(request, pk):
    historiques = EnrollementHistory.objects.filter(original_id=pk)  # objet_id = ID lié
    return render(request, 'role/histo_modif_enrollements.html', {'page_obj': historiques, 'original_id': pk})

def historique_modifications_decisions(request, pk):
    historiques = DecisionHistory.objects.filter(original_id=pk)  # objet_id = ID lié
    return render(request, 'role/histo_modif_decisions.html', {'historiques': historiques, 'original_id': pk})