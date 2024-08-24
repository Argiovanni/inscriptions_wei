# Create your views here.

from django import template
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import Inscrit,Bungalow
from .forms import PaiementCautionForm, PaiementPlaceForm, LoginForm


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
    return HttpResponse("You're looking at Bungalow")


