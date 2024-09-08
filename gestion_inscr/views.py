# Create your views here.

from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.storage import default_storage
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
import csv
import os
from site_wei.settings import BASE_DIR
from .models import Inscrit,Bungalow
from .forms import PaiementCautionForm, PaiementPlaceForm, LoginForm, AddMemberForm, MontantCautionForm, CsvFileForm


def index(request):
    context = {}
    return render(request,"index.html", context)


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'
    return render(request, "login.html", {"form": form, "msg": msg})

@login_required(login_url="/login/")
def inscrit(request):
    user = request.user #current user
    form_place = PaiementPlaceForm()
    form_caution = PaiementCautionForm()
    if request.method == 'POST':
        if 'paiement' in request.POST:
            participant = Inscrit.objects.get(id=request.POST.get('Participant'))
            statut_place = request.POST.get('paiement')[0]
            participant.payer_place(statut_place,user.username)
            
        if 'caution' in request.POST:
            participant = Inscrit.objects.get(id=request.POST.get('Participant'))
            statut_caution = request.POST.get('caution')[0]
            participant.payer_caution(statut_caution,user.username)
        
        if 'decharge' in request.POST:
            participant = Inscrit.objects.get(id=request.POST.get('decharge'))
            participant.update_decharge()
        
    qs = Inscrit.objects.all()
    context = {'inscrits' : qs, 'form_pl' : form_place, 'form_c' : form_caution}
    return render(request, "inscription.html", context)


@login_required(login_url="/login/")
def bungalow(request):
    user = request.user
    form_member = AddMemberForm()
    form_montant_caution = MontantCautionForm
    if request.method == 'POST':
        if 'rendre_caution' in request.POST:
            bungalow = Bungalow.objects.get(id=request.POST.get("rendre_caution"))
            for membre in bungalow.get_members():
                membre.rendre_caution()
            bungalow.caution_total = 0.0
            bungalow.save()
            
        if 'montant' in request.POST:
            bungalow = Bungalow.objects.get(id=request.POST.get("Bungalow"))
            prix = float(request.POST.get('montant'))
            bungalow.substract_from_caution(prix)
            
        if 'participant' in request.POST:
            bungalow = Bungalow.objects.get(id=request.POST.get("Bungalow"))
            participant_id = int(request.POST.get('participant'))
            bungalow.add_pers(Inscrit.objects.get(id=participant_id))
            
    qs = Bungalow.objects.all()
    context={'bungalows' : qs, 'form_m' : form_member, 'form_d' : form_montant_caution}
    return render(request,"bungalow.html",context)


def add_inscrit_from_csv(file_name):
    print("start script")
    csvfile = default_storage.open(file_name, 'r')
    reader = csv.reader(csvfile, delimiter=';')
    next(reader, None) # skip header
    nb_created = 0
    for row in reader:
        nom_prenom = row[1].split()
        prenom = nom_prenom[0]
        nom = ' '.join(nom_prenom[1:])
        if not nom.strip():
            nom = "------"
            
        if row[3] == "Oui":
            place_paye = True
        else :
            place_paye = False
            
        type_paiement = row[7]
        if type_paiement == "Lydia" :
            paiement = 'L'
        elif type_paiement == "Cash" :
            paiement = 'E'
        else : # chèque
            paiement = 'C'
            
        type_billet = row[8]
        if ("Non cotisants" in type_billet):
            billet = 'N'
        else:
            billet = 'O'
            
        if row[9] == "Oui":
            cotise_AE = True
        else :
            cotise_AE = False
            
        # should not be usefull but let it here for now
        if (billet == 'O') and not cotise_AE:
            comment = "/!\ need payer cotisation"
        else :
            comment = None
            
        filiere = row[10]
        if not filiere.strip():
            filiere = "AUX"
            
        promo = row[11]
        if not promo.strip():
            promo = "V"
            
        if promo == "1A":
            caution = 100.0
        else :
            caution = 200.0
        
        # prix 
        prix = float(row[15])
        code_billet = row[13]
        try:
            inscrit_obj = Inscrit.objects.get(code_billet=code_billet)
        except Inscrit.DoesNotExist:
            inscrit_obj = None
        if inscrit_obj:
            # inscrit exist in DB
            pass
        else:
            if row[6] == "Oui":
                # place annulée
                pass
            else:
                inscrit_obj = Inscrit.objects.create(nom=nom,prenom=prenom,promo=promo,filier=filiere,
                            cautisant=cotise_AE, prix_place=prix,paiement=paiement,place_paye=place_paye,
                            code_billet=code_billet,valeur_caution= caution, type_billet=billet, commentaires=comment)
                nb_created += 1
                print("created inscrit : ", inscrit_obj)
    print("nb inscrit objects created : ", nb_created)



@staff_member_required
def update_db_from_csv(request):
    if request.method == 'GET':
        form = CsvFileForm()
    
    if request.method == 'POST':
        print("POST")
        form = CsvFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return redirect("/")
            if csv_file.multiple_chunks():
                messages.error(request, 'Uploaded file is too big (%.2f MB)' %(csv_file.size(1000*1000),))
                return redirect("/")
            filename = default_storage.save(csv_file.name, csv_file)
        
            add_inscrit_from_csv(filename)
            messages.success("data uploaded to DB !")
            return redirect("/")
            
            
    return render(request, "updateDB.html", {"form" : form})