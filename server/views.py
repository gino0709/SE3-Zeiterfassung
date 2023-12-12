from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
import os
from django.conf import settings
from datetime import date, datetime
import json
import csv
import hashlib
from django.shortcuts import render, redirect

# Create your views here.
def home(request):
    ausgabe = "<html><body><h3>Hallo! Willkommen auf meiner neuen WebApp :)</h3></body></html>"
    return HttpResponse(ausgabe)

def startseite(request):
    keks = request.COOKIES.get("cookie_username", False)

    nutzerRolle = ""
    
    userZeiten = zeitenDatei(keks)

    with open("/home/ubuntu/django-test/newApp/templates/newApp/module.json", "r") as dateiM:
        auslesen = dateiM.read()
        verfuegbareModule = json.loads(auslesen)
        erlaubteModule = list()
        for modul in verfuegbareModule:
            if verfuegbareModule[modul] == True:
                erlaubteModule.append(modul)

    with open("/home/ubuntu/django-test/newApp/templates/newApp/nutzerDatenbank.json", "r") as dateiD:
        auslesen = dateiD.read()
        deserialisierteNutzer = json.loads(auslesen)
    
    for user in deserialisierteNutzer:
        if user["Mail"] == keks:
            nutzerRolle = user["Rolle"]
#Neue Buchung erstellen
    if request.method == 'POST':
        if request.POST.get("abschicken") == "buchen":
            neueBuchung(request)

            if nutzerRolle == "anwender":
                return render(request, 'newApp/startseiteAnwender.html',{
                    "zeiten": userZeiten,
                    "module": erlaubteModule,
                })
            elif nutzerRolle == "vip":
                return render(request, 'newApp/startseiteVip.html',{
                    "zeiten": userZeiten,
                    "module": erlaubteModule,
                })
            elif nutzerRolle == "admin":
                return render(request, 'newApp/startseiteVip.html',{
                    "zeiten": userZeiten,
                    "module": erlaubteModule,
                })

#Aktualisieren
        elif request.POST.get("abschicken") == "aktualisieren":
            return redirect("http://193.196.55.232:8888/newApp/Startseite/")
    
#Buchung löschen
        elif request.POST.get("abschicken") == "loeschen":
            beitragLoeschen(request)

            if nutzerRolle == "anwender":
                return render(request, 'newApp/startseiteAnwender.html',{
                    "zeiten": userZeiten,
                    "module": erlaubteModule,
                })
            elif nutzerRolle == "vip":
                return render(request, 'newApp/startseiteVip.html',{
                    "zeiten": userZeiten,
                    "module": erlaubteModule,
                })
            elif nutzerRolle == "admin":
                return render(request, 'newApp/startseiteVip.html',{
                    "zeiten": userZeiten,
                    "module": erlaubteModule,
                })
        
#Buchungen filtern
        elif request.POST.get("abschicken") == "filtern":
            zeiten = filtern(request)

            if nutzerRolle == "anwender":
                return render(request, 'newApp/startseiteAnwender.html',{
                    "zeiten": zeiten,
                    "module": erlaubteModule,
                })
            elif nutzerRolle == "vip":
                return render(request, 'newApp/startseiteVip.html',{
                    "zeiten": zeiten,
                    "module": erlaubteModule,
                })
            elif nutzerRolle == "admin":
                return render(request, 'newApp/startseiteVip.html',{
                    "zeiten": zeiten,
                    "module": erlaubteModule,
                })

#Weiterleitung von Anmelden auf Startseite
    if nutzerRolle == "anwender":
        return render(request, 'newApp/startseiteAnwender.html',{
            "zeiten": userZeiten,
            "module": erlaubteModule,
        })
    elif nutzerRolle == "vip":
        return render(request, 'newApp/startseiteVip.html',{
            "zeiten": userZeiten,
            "module": erlaubteModule,
        })
    elif nutzerRolle == "admin":
                return render(request, 'newApp/startseiteVip.html',{
                    "zeiten": userZeiten,
                    "module": erlaubteModule,
        })
            
def getBaseDir(request):
    return HttpResponse(settings.BASE_DIR)

#------------------------------------------------------------------------------------------------------------

class Nutzer:
    def __init__(self, mail, password):
        self.__rolle = "anwender"
        self.__mail = mail
        self.__password = password
        self.__sperrung = False
        self.__dateiname = f"{self.__mail}.json"

        with open("/home/ubuntu/django-test/newApp/templates/newApp/nutzerDatenbank.json", "r") as datei0:
            auslesen = datei0.read()
            deserialisierteNutzer = json.loads(auslesen)

            nutzer_info = {
            "Rolle": self.__rolle,
            "Mail": self.__mail,
            "Password": self.__password,
            "Sperrung": self.__sperrung,
            "dateiname": self.__dateiname,
            }
            deserialisierteNutzer.append(nutzer_info)

        with open("/home/ubuntu/django-test/newApp/templates/newApp/nutzerDatenbank.json", "w") as datei1:
            json.dump(deserialisierteNutzer, datei1, indent=2)

        with open(f"/home/ubuntu/django-test/newApp/templates/newApp/{self.__dateiname}", "w") as datei2:
            datei2.write("{}")

    def __repr__(self):
        return self.__mail
    
    def gebeMail(self):
        return self.__mail
    
    def gebeDateinamen(self):
        return self.__dateiname    

def filtern(request):
    tag = request.POST.get("filterTag")
    modul = request.POST.get("filterModul")

    keks = request.COOKIES.get("cookie_username", False)
    userZeiten = zeitenDatei(keks)

    gefilterteZeiten = dict()

    if tag == "Alle Tage":
        if modul == "Alle Module":
            return userZeiten
        elif modul != "Alle Module":
            for tag in userZeiten:
                gefilterteZeiten[tag] = dict()
                if modul in userZeiten[tag]:
                    gefilterteZeiten[tag][modul] = userZeiten[tag][modul]
    
    elif tag != "Alle Tage":
        if modul == "Alle Module":
            for eintragTag in userZeiten:
                if eintragTag == tag:
                    gefilterteZeiten[tag] = userZeiten[tag]
        elif modul != "Alle Module":
            for eintragTag in userZeiten:
                if eintragTag == tag:
                    gefilterteZeiten[tag] = dict()
                    for eintragModul in userZeiten[eintragTag]:
                        if eintragModul == modul:
                            gefilterteZeiten[tag][modul] = userZeiten[tag][modul]
                 
    return gefilterteZeiten


def zeitenDatei(nutzer):
    with open("/home/ubuntu/django-test/newApp/templates/newApp/nutzerDatenbank.json", "r") as dateiD:
        auslesen = dateiD.read()
        deserialisierteNutzer = json.loads(auslesen)
    
    for user in deserialisierteNutzer:
        if user["Mail"] == nutzer:
            dateiMitZeiten = user["dateiname"]

    with open("/home/ubuntu/django-test/newApp/templates/newApp/" + dateiMitZeiten, "r") as dateiJ:
        inhalt = dateiJ.read()
        deserialisierterInhalt = json.loads(inhalt)
        return deserialisierterInhalt

def registratur(request):
    if request.method == 'POST':
        registratur = request.POST.get("Rmail")
        anmeldung = request.POST.get("Amail")
        Apassword = request.POST.get("pw")

        with open("/home/ubuntu/django-test/newApp/templates/newApp/nutzerDatenbank.json", "r") as datei0:
            auslesen = datei0.read()
            deserialisierteNutzer = json.loads(auslesen)
#ANMELDEN
        if request.POST.get("bestätigen") == "anmelden":
            for nutzer in deserialisierteNutzer:
                if nutzer["Sperrung"] == False:
                    if nutzer["Mail"] == anmeldung:
                        ApasswordGehasht = hashlib.sha256(Apassword.encode("utf-8")).hexdigest()
                        if nutzer["Password"] == ApasswordGehasht:
                            
                            if nutzer["Rolle"] == "anwender":
                                response = redirect("http://193.196.55.232:8888/newApp/Startseite/")
                                response.set_cookie("cookie_username", anmeldung)
                                return response

                            elif nutzer["Rolle"] == "vip":
                                response = redirect("http://193.196.55.232:8888/newApp/Startseite/")
                                response.set_cookie("cookie_username", anmeldung)
                                return response

                            elif nutzer["Rolle"] == "admin":
                                response = redirect("http://193.196.55.232:8888/newApp/Startseite/")
                                response.set_cookie("cookie_username", anmeldung)
                                return response
                        
                        else:
                            return HttpResponse("Sie haben das falsche Passwort eingegeben!")
                else:
                    return HttpResponse("Sie wurden durch einen Admin gesperrt!")
#REGISTRIEREN
        elif request.POST.get("bestätigen") == "registrieren":
            for nutzer in deserialisierteNutzer:
                if nutzer["Mail"] == registratur:
                    return HttpResponse("E-Mail schon vorhanden. Bitte anmelden!")

            pw1 = request.POST.get("pw")
            pw2 = request.POST.get("pwBestätigen")

            pw1Gehasht = hashlib.sha256(pw1.encode("utf-8")).hexdigest()
            pw2Gehasht = hashlib.sha256(pw2.encode("utf-8")).hexdigest()

            if pw1Gehasht == pw2Gehasht:
                legeNutzerAn = Nutzer(registratur, pw1Gehasht)
            else:
                return HttpResponse("Passwörter stimmen nicht überein")

    return render(request, "newApp/registratur.html")

def neueBuchung(request):
            buchungstag = request.POST.get("user_date")
            buchungsstart = request.POST.get("user_start")
            buchungsende = request.POST.get("user_ende")
            
            start = datetime.strptime(buchungsstart, "%H:%M")
            ende = datetime.strptime(buchungsende, "%H:%M")
            buchungszeit = ende - start
            buchungMin = buchungszeit.total_seconds() / 60
            
            buchungsmodul = request.POST.get("auswahlModul")
            buchungsbericht = request.POST.get("user_bericht")

            keks = request.COOKIES.get("cookie_username", False)
            userZeiten = zeitenDatei(keks)
    
            if buchungstag not in userZeiten:
                userZeiten[buchungstag] = dict()
            if buchungsmodul not in userZeiten[buchungstag]:
                userZeiten[buchungstag][buchungsmodul] = list()
            neuerDictEintrag = dict()
            neuerDictEintrag["arbeitszeit"] = int(buchungMin)
            neuerDictEintrag["bericht"] = buchungsbericht
            userZeiten[buchungstag][buchungsmodul].append(neuerDictEintrag)

            sortierteZeiten = dict(sorted(userZeiten.items()))
            gedumpteVersion = json.dumps(sortierteZeiten)

            with open(f"/home/ubuntu/django-test/newApp/templates/newApp/{keks}.json", "w") as datei2:
                datei2.write(gedumpteVersion)

def beitragLoeschen(request):
    tag = request.POST.get("loeschTag")
    modul = request.POST.get("loeschModul")
    arbeitszeit = request.POST.get("loeschArbeitszeit")
    bericht = request.POST.get("loeschBericht")

    keks = request.COOKIES.get("cookie_username", False)
    userZeiten = zeitenDatei(keks)

    if tag in userZeiten:
        if modul in userZeiten[tag]:
            anzahlDerBuchungenImModul = len(userZeiten[tag][modul])
            if anzahlDerBuchungenImModul == 1:
                del userZeiten[tag][modul]                              #entfernt den Key mit value
                zähler = 0
                for key in userZeiten[tag]:
                    zähler += 1
                if zähler == 0:
                    del userZeiten[tag]
            else:
                for buchung in userZeiten[tag][modul]:
                    if buchung["arbeitszeit"] == int(arbeitszeit):
                        if buchung["bericht"] == bericht:
                            userZeiten[tag][modul].remove(buchung)
    
    gedumpteVersion = json.dumps(userZeiten)

    with open(f"/home/ubuntu/django-test/newApp/templates/newApp/{keks}.json", "w") as datei:
        datei.write(gedumpteVersion)




"""
Wie viele Personen verwenden welchen e-Mail Provider (prozentuell)?
Welcher e-Mail Provider ist am beliebtesten je nach Gender?
def beliebtesterProviderEinesGeschlechts(genderAlsString, pfadZurCsv):
    hoechsterWert = 0
    mostUsedProvider = ""
    alleProvider = dict()
    with open(pfadZurCsv, "r") as csvDatei:
        reader = csv.reader(csvDatei)
        next(reader)

        for row in reader:
            rowGender = row[1]
            rowProvider = row[0]
            splittung = rowProvider.split("@")
            rowProvider = splittung[1]
            if rowGender == genderAlsString:
                if rowProvider not in alleProvider:
                    alleProvider[rowProvider] = 1
                else:
                    alleProvider[rowProvider] += 1
        for provider in alleProvider:
            if alleProvider[provider] > hoechsterWert:
                hoechsterWert = alleProvider[provider]
                mostUsedProvider = provider
    return (hoechsterWert, mostUsedProvider)

def csvInJsonFormatieren(request):
# --------------------------  Part 1 --------------------------  
    with open("/home/ubuntu/django-test/newApp/templates/newApp/mockDaten.csv", "r") as dateiC:
        reader = csv.reader(dateiC)
        next(reader)

        alleEmailProvider = 0
        einzelneEmailProvider = dict()
        for row in reader:
            mail = row[0]
            teilung = mail.split("@")
            emailProvider = teilung[1]
            if emailProvider not in einzelneEmailProvider:
                einzelneEmailProvider[emailProvider] = 1
            else:
                einzelneEmailProvider[emailProvider] += 1
            alleEmailProvider += 1

    for eintrag in einzelneEmailProvider:
        prozentsatz = (einzelneEmailProvider[eintrag] * 100 / alleEmailProvider)
        einzelneEmailProvider[eintrag] = prozentsatz
        einzelneEmailProvider[eintrag] = str(prozentsatz) + "%"

  # --------------------------  Part 2 --------------------------  
    with open("/home/ubuntu/django-test/newApp/templates/newApp/mockDaten.csv", "r") as dateiC2:
        reader = csv.reader(dateiC2)
        next(reader)
        dictMitAllenGendern = dict()
        for row in reader:
            mail = row[0]
            teilung = mail.split("@")
            emailProvider = teilung[1]
            gender = row[1]
            meinDict = dict()
            if gender not in dictMitAllenGendern:
                dictMitAllenGendern[gender] = meinDict

            if emailProvider not in dictMitAllenGendern[gender]:
                dictMitAllenGendern[gender][emailProvider] = 1 
            else:
                dictMitAllenGendern[gender][emailProvider] += 1
            
        ausgabeDict = dict()
        for gender in dictMitAllenGendern:
            _, providerName = beliebtesterProviderEinesGeschlechts(gender, "/home/ubuntu/django-test/newApp/templates/newApp/mockDaten.csv")
            ausgabeDict[gender] = providerName
        
            # ALTERNATIV ANSTATT DER FUNKTION:
            # hoechsterWert = 0
            # mostUsedProvider = ""
            # for provider in dictMitAllenGendern[gender]:
            #     if dictMitAllenGendern[gender][provider] > hoechsterWert:
            #         hoechsterWert = dictMitAllenGendern[gender][provider]
            #         mostUsedProvider = provider
            # ausgabeDict[gender] = [hoechsterWert, mostUsedProvider]
            
    for geschlecht in ausgabeDict:
        myProvider = ausgabeDict[geschlecht]
        einzelneEmailProvider[geschlecht] = myProvider

# --------------------------  Serialisierung des DICT & Ausgabe per json-Download --------------------------  
    serialisiertesDict = json.dumps(einzelneEmailProvider)
    with open("/home/ubuntu/django-test/newApp/templates/newApp/mockDaten.json", "w") as dateiJ:
        dateiJ.write(serialisiertesDict)
            
    response = HttpResponse(serialisiertesDict, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="mockDaten.json"'

    return response
"""
