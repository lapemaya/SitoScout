from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Conto, Spesa, Persona
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def home_page(request):
    return render(request, 'home.html')


def action(request):
    return render(request, 'action.html')

def calculator(request):
    if request.method == 'POST':
        cost_per_night = request.POST.get('cost_per_night')
        number_person = request.POST.get('number-person')
        number_capi = request.POST.get('number-capi')
        number_cambu = request.POST.get('number-cambu')
        number_pasti = request.POST.get('number-pasti')
        number_break = request.POST.get('number-break')
        materiale = request.POST.get('materiale')
        attivo = request.POST.get('attivo')
        number_night = request.POST.get('number-night')

        capi_pagano= request.POST.get('capi-pagano')
        cambu_pagano= request.POST.get('cambu-quota')
        capi_casa= request.POST.get('capi-casa')
        cambu_casa= request.POST.get('cambu-pagano')

        if(capi_casa=="on"):
            capi_casa=True
        else:
            capi_casa=False

        if (cambu_casa == "on"):
            cambu_casa = True
        else:
            cambu_casa = False

        if (cambu_pagano == "on"):
            cambu_pagano = True
        else:
            cambu_pagano = False

        if (capi_pagano == "on"):
            capi_pagano = True
        else:
            capi_pagano = False



        cost_per_night = float(cost_per_night)
        number_person = float(number_person)
        number_capi = float(number_capi)
        number_cambu = float(number_cambu)
        number_pasti = float(number_pasti)
        materiale = float(materiale)
        attivo = float(attivo)
        number_night = float(number_night)
        number_break = float(number_break)

        partecipanti=number_person+number_capi+number_cambu
        paganti=number_person+number_capi*capi_pagano+number_cambu*cambu_pagano
        persone_casa=number_person+number_capi*capi_casa+number_cambu*cambu_casa

        spesa=persone_casa*cost_per_night*number_night+partecipanti*number_pasti*3.5+partecipanti*number_break*3.5/2 +materiale+attivo
        quota=spesa/paganti

        spesa=round(spesa,2)
        quota=round(quota,2)

        return JsonResponse({
            'status': 'success',
            'spesa': spesa,
            'quota': quota
        })
    return render(request, 'calculator.html')

def conti(request):
    conto = Conto.objects.get(user=request.user)
    if request.method== 'POST':
        tipoConto = request.POST.get('tipoConto')
        operazione = request.POST.get('operazione')
        valore = request.POST.get('valore')


        valore = float(valore)
        if(tipoConto=="carta"):
            if(operazione=="incremento"):
                conto.carta+=valore
            else:
                conto.carta-=valore

        if (tipoConto == "cash"):
            if (operazione == "incremento"):
                conto.cash += valore
            else:
                conto.cash -= valore

        if (tipoConto == "conto"):
            if (operazione == "incremento"):
                conto.conto += valore
            else:
                conto.conto -= valore
        conto.save()
    return render(request, 'conti.html',{"carta":conto.carta,"cash":conto.cash,"conto":conto.conto})


def login_page(request):
    if request.method=="POST":
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            return render(request,"action.html") # Reindirizza alla dashboard o ad altre pagine
        return render(request, "login.html",{"message":"Username o password errati"})
    return render(request,"login.html")

def create_user(request):
    if(request.method=="POST"):
        nuovo = User.objects.filter(username=request.POST.get("username"))
        if not nuovo.exists():
            if request.POST.get("password")==request.POST.get("confirm_password"):
                ciao = User.objects.create_user(username=request.POST.get("username"),
                                                 password=request.POST.get("password"),email=request.POST.get("email"))
                login(request,ciao)
                conto=Conto.objects.create(user=ciao)
                return render(request,"action.html")
            else:
                return render(request, "create_user.html",{"message":"Le password non corrispondono"})
        else:
            return render(request, "create_user.html", {"message": "Username già in uso"})
    return render(request,"create_user.html")

def contability(request):
    spese = Spesa.objects.all()  # Recupera tutte le spese dal database
    return render(request,"contability.html",{"spese":spese})

def creazioneSpesa(request):
    if request.method=="POST":
        if(request.POST.get('flexRadioDefault')=="carta"):
            spesa=Spesa.objects.create(user=request.user,cosa=request.POST.get("cosa"),dove=request.POST.get("dove"),data=request.POST.get("data"),quanto=request.POST.get("quanto"),cartacash=False)
            conto=Conto.objects.get(user=request.user)
            conto.carta-=float(request.POST.get("quanto"))
            conto.save()
        else:
            spesa=Spesa.objects.create(user=request.user,cosa=request.POST.get("cosa"),dove=request.POST.get("dove"),data=request.POST.get("data"),quanto=request.POST.get("quanto"),cartacash=True)
            conto = Conto.objects.get(user=request.user)
            conto.cash -= float(request.POST.get("quanto"))
            conto.save()
        if(request.POST.get("note")):
            spesa.note=request.POST.get("note")
        return redirect("contability")
    return render(request,"creazioneSpesa.html")

def modificaSpesa(request, id):
    spesa = Spesa.objects.get(id=id)
    oldcartacash=spesa.cartacash
    oldquanto=spesa.quanto
    if(request.method=="POST"):
        spesa.cosa=request.POST.get("cosa")
        spesa.dove=request.POST.get("dove")
        spesa.data=request.POST.get("data")
        spesa.quanto=request.POST.get("quanto")
        if (request.POST.get('flexRadioDefault') == "carta"):
            spesa.cartacash=False
        else:
            spesa.cartacash = True
        if (request.POST.get("note")):
            spesa.note = request.POST.get("note")
        spesa.save()

        conto = Conto.objects.get(user=request.user)
        if oldcartacash==spesa.cartacash :
            if not oldquanto == float(spesa.quanto):
                if not spesa.cartacash:
                    conto.carta+=(oldquanto-float(spesa.quanto))
                else:
                    conto.cash += (oldquanto - float(spesa.quanto))
        if not oldcartacash==spesa.cartacash :
            if oldquanto==float(spesa.quanto):
                if not oldcartacash:
                    conto.carta+=oldquanto
                    conto.cash-=oldquanto
                else:
                    conto.carta -= oldquanto
                    conto.cash += oldquanto
            if not oldquanto==float(spesa.quanto):
                if not oldcartacash:
                    conto.carta += oldquanto
                    conto.cash -= float(spesa.quanto)
                else:
                    conto.carta -= float(spesa.quanto)
                    conto.cash += oldquanto
        conto.save()
        return redirect("contability")
    return render(request, "modificaSpesa.html", {"spesa": spesa})

def eliminaspesa(request,id):
    spesa = Spesa.objects.get(id=int(id))
    if not spesa.cartacash:
        conto = Conto.objects.get(user=request.user)
        conto.carta+=spesa.quanto
        conto.save()
    else:
        conto = Conto.objects.get(user=request.user)
        conto.cash += spesa.quanto
        conto.save()
    spesa.delete()

    return render(request,"contability.html")

def branco(request):
    persone = Persona.objects.all()
    return render(request, "branco.html", {"persone": persone})

def creazionePersona(request):
    if request.method=="POST":
        if(request.POST.get('flexRadioDefault')=="maschio"):
            persona=Persona.objects.create(user=request.user,nome=request.POST.get("nome"),cognome=request.POST.get("cognome"),data=request.POST.get("data"),sex=False)
        else:
            persona=Persona.objects.create(user=request.user,nome=request.POST.get("nome"),cognome=request.POST.get("cognome"),data=request.POST.get("data"),sex=True)
        if(request.POST.get("note")):
            persona.note=request.POST.get("note")
        return redirect("branco")
    return render(request, "creazionePersona.html")

def modificaPersona(request,id):
    persona = Persona.objects.get(id=id)
    if (request.method == "POST"):
        persona.nome = request.POST.get("nome")
        persona.cognome = request.POST.get("cognome")
        persona.data = request.POST.get("data")
        if (request.POST.get('flexRadioDefault') == "maschio"):
            persona.sex = False
        else:
            persona.sex = True
        if (request.POST.get("note")):
            persona.note = request.POST.get("note")
        persona.save()
        return redirect("branco")
    return render(request, "modificaPersona.html",{"persona": persona})


def eliminaPersona(request,id):
    persona = Persona.objects.get(id=int(id))
    persona.delete()
    return render(request, "branco.html")
