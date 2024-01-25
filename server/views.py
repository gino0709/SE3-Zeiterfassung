from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
import os
from django.conf import settings
from datetime import date, datetime
import json
import csv
from lxml import etree
import hashlib
from django.shortcuts import render, redirect
import requests

from django.http import FileResponse

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
        alleModule = list()
        for modul in verfuegbareModule:
            alleModule.append(modul)
            if verfuegbareModule[modul] == True:
                erlaubteModule.append(modul)

    deserialisierteNutzer = nutzerDatenbankAuslesen() 

    for user in deserialisierteNutzer:
        if user["Mail"] == keks:
            nutzerRolle = user["Rolle"]
#Neue Buchung erstellen
    if request.method == 'POST':
        if request.POST.get("abschicken") == "buchen":
            neueBuchung(request)
            neueZeiten = zeitenDatei(keks)

            if nutzerRolle == "anwender":
                return render(request, 'newApp/startseiteAnwender.html',{
                    "zeiten": neueZeiten,
                    "moduleAlle": alleModule,
                    "moduleFrei": erlaubteModule,
                })
            elif nutzerRolle == "vip":
                return render(request, 'newApp/startseiteVip.html',{
                    "zeiten": neueZeiten,
                    "moduleAlle": alleModule,
                    "moduleFrei": erlaubteModule,
                })
            elif nutzerRolle == "admin":
                return render(request, 'newApp/startseiteAdmin.html',{
                    "zeiten": neueZeiten,
                    "moduleAlle": alleModule,
                    "moduleFrei": erlaubteModule,
                })
#Buchung löschen
        elif request.POST.get("abschicken") == "loeschen":
            beitragLoeschen(request)
            neueZeiten = zeitenDatei(keks)

            if nutzerRolle == "anwender":
                return render(request, 'newApp/startseiteAnwender.html',{
                    "zeiten": neueZeiten,
                    "moduleAlle": alleModule,
                    "moduleFrei": erlaubteModule,
                })
            elif nutzerRolle == "vip":
                return render(request, 'newApp/startseiteVip.html',{
                    "zeiten": neueZeiten,
                    "moduleAlle": alleModule,
                    "moduleFrei": erlaubteModule,
                })
            elif nutzerRolle == "admin":
                return render(request, 'newApp/startseiteAdmin.html',{
                    "zeiten": neueZeiten,
                    "moduleAlle": alleModule,
                    "moduleFrei": erlaubteModule,
                })
#Buchungen filtern
        elif request.POST.get("abschicken") == "filtern":
            zeiten = filtern(request)

            if nutzerRolle == "anwender":
                return render(request, 'newApp/startseiteAnwender.html',{
                    "zeiten": zeiten,
                    "moduleAlle": alleModule,
                    "moduleFrei": erlaubteModule,
                })
            elif nutzerRolle == "vip":
                return render(request, 'newApp/startseiteVip.html',{
                    "zeiten": zeiten,
                    "moduleAlle": alleModule,
                    "moduleFrei": erlaubteModule,
                })
            elif nutzerRolle == "admin":
                return render(request, 'newApp/startseiteAdmin.html',{
                    "zeiten": zeiten,
                    "moduleAlle": alleModule,
                    "moduleFrei": erlaubteModule,
                })
#Weiterleitung zur Übersicht
        elif request.POST.get("abschicken") == "uebersicht":
            uebergabe = zeitenberechnung(request)
            return render(request, 'newApp/uebersicht.html',{
                "output": uebergabe,
                "mailCookie": keks,
            })
#Vip Bewerbung
        elif request.POST.get("abschicken") == "vipAnfrage":
            vipBewerbung(request)
#Admin Bewerbung
        elif request.POST.get("abschicken") == "adminAnfrage":
            adminBewerbung(request)
#Anfragen bearbeiten
        elif request.POST.get("abschicken") == "anfragen":
            alleAnfragen = anfragenBearbeiten(request)
            return render(request, 'newApp/anfragen.html',{
                "nutzeranfragenVip": alleAnfragen[0],
                "nutzeranfragenAdmin": alleAnfragen[1],
            })
#Anfrage genehmigen
        elif request.POST.get("abschicken") == "genehmigen":
            genehmigung(request)
            alleAnfragen = anfragenBearbeiten(request)
            return render(request, 'newApp/anfragen.html',{
                "nutzeranfragenVip": alleAnfragen[0],
                "nutzeranfragenAdmin": alleAnfragen[1],
            })
#Anfrage ablehnen
        elif request.POST.get("abschicken") == "ablehnen":
            ablehnung(request)
            alleAnfragen = anfragenBearbeiten(request)
            return render(request, 'newApp/anfragen.html',{
                "nutzeranfragenVip": alleAnfragen[0],
                "nutzeranfragenAdmin": alleAnfragen[1],
            })
#Download der verschiedenen Formate
        elif request.POST.get("abschicken") == "download":
            fileFormat = request.POST.get("format")
            if fileFormat == "xmlDownload":
                response = redirect("http://193.196.55.232:8888/newApp/downloads.xml")
                return response
            elif fileFormat == "jsonDownload":
                response = redirect("http://193.196.55.232:8888/newApp/downloads.json")
                return response
            elif fileFormat == "csvDownload":
                response = redirect("http://193.196.55.232:8888/newApp/downloads.csv")
                return response
#Upload der verschiedenen Formate
        elif request.POST.get("abschicken") == "upload":
            datei_upload(request)
            neueZeiten = zeitenDatei(keks)
            if nutzerRolle == "vip":
                return render(request, 'newApp/startseiteVip.html',{
                    "zeiten": neueZeiten,
                    "moduleAlle": alleModule,
                    "moduleFrei": erlaubteModule,
                })
            elif nutzerRolle == "admin":
                return render(request, 'newApp/startseiteAdmin.html',{
                    "zeiten": neueZeiten,
                    "moduleAlle": alleModule,
                    "moduleFrei": erlaubteModule,
                })
#Userübersicht 
        elif request.POST.get("abschicken") == "userUebersicht":
            alleUser = uebersichtVorhandeneUser(request)
            return render(request, 'newApp/userUebersicht.html',{
                "gesperrteUser": alleUser[0],
                "aktiveUser": alleUser[1],
            })
#User sperren
        elif request.POST.get("abschicken") == "userSperren":
            userMail = request.POST.get("userMail")
            userSperren(request, userMail)
            alleUser = uebersichtVorhandeneUser(request)
            return render(request, 'newApp/userUebersicht.html',{
                "gesperrteUser": alleUser[0],
                "aktiveUser": alleUser[1],
            })
#User freigeben
        elif request.POST.get("abschicken") == "userFreigeben":
            userMail = request.POST.get("userMail")
            userFreigeben(request, userMail)
            alleUser = uebersichtVorhandeneUser(request)
            return render(request, 'newApp/userUebersicht.html',{
                "gesperrteUser": alleUser[0],
                "aktiveUser": alleUser[1],
            })
#Modulübersicht
        elif request.POST.get("abschicken") == "modulUebersicht":
            alleModule = uebersichtModule(request)
            return render(request, 'newApp/moduleUebersicht.html',{
                "gesperrteModule": alleModule[0],
                "aktiveModule": alleModule[1],
            })
#Modul freischalten
        elif request.POST.get("abschicken") == "modulFreischalten":
            modul = request.POST.get("modul")
            modulFreischalten(request, modul)
            alleModule = uebersichtModule(request)
            return render(request, 'newApp/moduleUebersicht.html',{
                "gesperrteModule": alleModule[0],
                "aktiveModule": alleModule[1],
            })
#Modul sperren
        elif request.POST.get("abschicken") == "modulSperren":
            modul = request.POST.get("modul")
            modulSperren(request, modul)
            alleModule = uebersichtModule(request)
            return render(request, 'newApp/moduleUebersicht.html',{
                "gesperrteModule": alleModule[0],
                "aktiveModule": alleModule[1],
            })
#Neues Modul freigeben
        elif request.POST.get("abschicken") == "neuesModul":
            modul = request.POST.get("newModul")
            neuesModul(request, modul)
            alleModule = uebersichtModule(request)
            return render(request, 'newApp/moduleUebersicht.html',{
                "gesperrteModule": alleModule[0],
                "aktiveModule": alleModule[1],
            })
#Logout
        elif request.POST.get("abschicken") == "logout":
            response = redirect("http://193.196.55.232:8888/newApp/registratur")
            response.delete_cookie("cookie_username")
            return response
#Weiterleitung von Anmelden auf Startseite
    if nutzerRolle == "anwender":
        return render(request, 'newApp/startseiteAnwender.html',{
            "zeiten": userZeiten,
            "moduleAlle": alleModule,
            "moduleFrei": erlaubteModule,
        })
    elif nutzerRolle == "vip":
        return render(request, 'newApp/startseiteVip.html',{
            "zeiten": userZeiten,
            "moduleAlle": alleModule,
            "moduleFrei": erlaubteModule,
        })
    elif nutzerRolle == "admin":
        return render(request, 'newApp/startseiteAdmin.html',{
            "zeiten": userZeiten,
            "moduleAlle": alleModule,
            "moduleFrei": erlaubteModule,
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

        deserialisierteNutzer = nutzerDatenbankAuslesen()

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
            datei2.write("[]")

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
    deserialisierteNutzer = nutzerDatenbankAuslesen()
    
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

        deserialisierteNutzer = nutzerDatenbankAuslesen()
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

def zeitenberechnung(request):
    keks = request.COOKIES.get("cookie_username", False)
    userZeiten = zeitenDatei(keks)
    
    uebersichtDict = {
        "Gesamt": {
            "Minuten": 0,
            },
    }
    for tag in userZeiten:
        for modul in userZeiten[tag]:
            if modul not in uebersichtDict:
                uebersichtDict[modul] = {"Minuten": 0}
            for buchung in userZeiten[tag][modul]:
                uebersichtDict[modul]["Minuten"] += buchung["arbeitszeit"]
                uebersichtDict["Gesamt"]["Minuten"] += buchung["arbeitszeit"]
    
    for key in uebersichtDict:
        if key == "Gesamt":
            uebersichtDict[key]["Prozente"] = 100
        if key != "Gesamt":
            prozentzahl = uebersichtDict[key]["Minuten"] / uebersichtDict["Gesamt"]["Minuten"] * 100
            uebersichtDict[key]["Prozente"] = "{:.2f}".format(prozentzahl)
    
    return uebersichtDict

def vipBewerbung(request):
    keks = request.COOKIES.get("cookie_username", False)
    with open("/home/ubuntu/django-test/newApp/templates/newApp/vipAnfragen.txt", "r") as datei:
        inhalt = datei.read()
        deserialisierterInhalt = json.loads(inhalt)
        if keks not in deserialisierterInhalt:
            deserialisierterInhalt.append(keks)
    inhalt = json.dumps(deserialisierterInhalt)
    with open("/home/ubuntu/django-test/newApp/templates/newApp/vipAnfragen.txt", "w") as datei:
        datei.write(inhalt)

def adminBewerbung(request):
    keks = request.COOKIES.get("cookie_username", False)
    with open("/home/ubuntu/django-test/newApp/templates/newApp/adminAnfragen.txt", "r") as datei:
        inhalt = datei.read()
        deserialisierterInhalt = json.loads(inhalt)
        if keks not in deserialisierterInhalt:
            deserialisierterInhalt.append(keks)
    inhalt = json.dumps(deserialisierterInhalt)
    with open("/home/ubuntu/django-test/newApp/templates/newApp/adminAnfragen.txt", "w") as datei:
        datei.write(inhalt)

def anfragenBearbeiten(request):    
    with open("/home/ubuntu/django-test/newApp/templates/newApp/vipAnfragen.txt", "r") as datei:
        inhalt = datei.read()
        deserialisierterInhaltVip = json.loads(inhalt)
    
    with open("/home/ubuntu/django-test/newApp/templates/newApp/adminAnfragen.txt", "r") as datei:
        inhalt = datei.read()
        deserialisierterInhaltAdmin = json.loads(inhalt)

    return [deserialisierterInhaltVip, deserialisierterInhaltAdmin]

def genehmigung(request):
    mailDesAntragsstellers = request.POST.get("anfrageMail")
    ablehnung(request)

    deserialisierterInhalt = nutzerDatenbankAuslesen()
    
    for user in deserialisierterInhalt:
        if user["Mail"] == mailDesAntragsstellers:
            if user["Rolle"] == "vip":
                user["Rolle"] = "admin"
            elif user["Rolle"] == "anwender":
                user["Rolle"] = "vip"
        else:
            None

    inhalt = json.dumps(deserialisierterInhalt)
    with open("/home/ubuntu/django-test/newApp/templates/newApp/nutzerDatenbank.json", "w") as datei:
        datei.write(inhalt)
    

def ablehnung(request):
    mailDesAntragsstellers = request.POST.get("anfrageMail")

    alleUser = nutzerDatenbankAuslesen()

    for user in alleUser:
        if user["Mail"] == mailDesAntragsstellers:

            if user["Rolle"] == "anwender":
                with open("/home/ubuntu/django-test/newApp/templates/newApp/vipAnfragen.txt", "r") as datei:
                    inhalt = datei.read()
                    deserialisierterInhalt = json.loads(inhalt)
                
                deserialisierterInhalt.remove(mailDesAntragsstellers)

                inhalt = json.dumps(deserialisierterInhalt)
                with open("/home/ubuntu/django-test/newApp/templates/newApp/vipAnfragen.txt", "w") as datei:
                    datei.write(inhalt)

            if user["Rolle"] == "vip":
                with open("/home/ubuntu/django-test/newApp/templates/newApp/adminAnfragen.txt", "r") as datei:
                    inhalt = datei.read()
                    deserialisierterInhalt = json.loads(inhalt)
                
                deserialisierterInhalt.remove(mailDesAntragsstellers)

                inhalt = json.dumps(deserialisierterInhalt)
                with open("/home/ubuntu/django-test/newApp/templates/newApp/adminAnfragen.txt", "w") as datei:
                    datei.write(inhalt)

def jsonInXml(request):
    keks = request.COOKIES.get("cookie_username", False)
    alleUser = nutzerDatenbankAuslesen()
    
    for user in alleUser:
        if user["Mail"] == keks:
            jsonDateiname = user["dateiname"]
    
    with open(f"/home/ubuntu/django-test/newApp/templates/newApp/{jsonDateiname}", "r") as jsondatei:
        dateiLesen = jsondatei.read()
        jsonlesen = json.loads(dateiLesen)
    
        buchungenE = etree.Element("Buchungen")
        for datum in jsonlesen:
            datumE = etree.Element("Datum")
            datumE.text = datum
            buchungenE.append(datumE)
            for modul in jsonlesen[datum]:
                modulE = etree.Element("Modul")
                modulE.text = modul
                datumE.append(modulE)
                for buchung in jsonlesen[datum][modul]:
                    berichtE = etree.Element("bericht")
                    berichtE.attrib["arbeitszeit"] = str(buchung["arbeitszeit"])
                    berichtE.text = buchung["bericht"]
                    modulE.append(berichtE)
        
        pfad = "/home/ubuntu/django-test/newApp/templates/newApp/downloadXmlFile.xml"
        root = etree.ElementTree(buchungenE)
        root.write(pfad, pretty_print=True, encoding="utf-8")
    
    return render(request, "newApp/downloadXmlFile.xml", content_type = 'data:text/xml;charset=utf-8,')

def jsonInCsv(request):
    keks = request.COOKIES.get("cookie_username", False)
    alleUser = nutzerDatenbankAuslesen()
    
    for user in alleUser:
        if user["Mail"] == keks:
            jsonDateiname = user["dateiname"]
    
    with open(f"/home/ubuntu/django-test/newApp/templates/newApp/{jsonDateiname}", "r") as jsondatei:
        dateiLesen = jsondatei.read()
        jsonlesen = json.loads(dateiLesen)
    
    with open("/home/ubuntu/django-test/newApp/templates/newApp/downloadCsvFile.csv", "w", newline="", encoding="utf-8") as csvdatei:
        csvschreiben = csv.writer(csvdatei, delimiter="|")
        kopfzeile = ["Datum", "Modul", "Arbeitszeit", "Bericht"]
        csvschreiben.writerow(kopfzeile)
        for datum in jsonlesen:
            for modul in jsonlesen[datum]:
                for buchung in jsonlesen[datum][modul]:
                    neueZeile = [datum, modul, buchung["arbeitszeit"], buchung["bericht"]]
                    csvschreiben.writerow(neueZeile)
    return render(request, "newApp/downloadCsvFile.csv", content_type = 'data:text/csv;charset=utf-8,')

def jsonDownload(request):
    keks = request.COOKIES.get("cookie_username", False)
    alleUser = nutzerDatenbankAuslesen()
    
    for user in alleUser:
        if user["Mail"] == keks:
            jsonDateiname = user["dateiname"]

    return render(request, f"newApp/{jsonDateiname}", content_type = "data:text/json;charset=utf-8,")

def datei_upload(request):
    keks = request.COOKIES.get("cookie_username", False)

    if request.method == 'POST' and request.FILES['myfile']:	
        myfile = request.FILES['myfile']						#file wird rausgeholt und als Variable gespeichert
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)					#abspeichern der Datei
        url = fs.url(filename)									#django generiert eine url

    alleUser = nutzerDatenbankAuslesen()

    if filename.endswith(".xml"):
        xmlUpload(request, filename)
    elif filename.endswith(".csv"):
        csvUpload(request, filename)
    elif filename.endswith(".json"):
        jsonUpload(request, filename)
    
    for user in alleUser:
        if user["Mail"] == keks:
            if user["Rolle"] == "vip":
                return render(request, '/home/ubuntu/django-test/newApp/templates/newApp/startseiteVip.html')
            if user["Rolle"] == "admin":
                return render(request, '/home/ubuntu/django-test/newApp/templates/newApp/startseiteAdmin.html')   

def xmlUpload(request, dateiName):
    keks = request.COOKIES.get("cookie_username", False)
    jsonInhalt = dict()

    pfad = os.path.join(settings.MEDIA_ROOT, dateiName)
    with open(pfad, "r", encoding="utf-8") as dateiX:
        lesen = dateiX.read()
    
    myXml = etree.fromstring(lesen)
    for buchung in myXml:
        datumB = buchung.text
        if datumB not in jsonInhalt:
            jsonInhalt[datumB] = dict()
            for modul in buchung:
                modulB = modul.text
                if modulB not in jsonInhalt[datumB]:
                    jsonInhalt[datumB][modulB] = list()
                for bericht in modul:
                    arbeitszeitB = bericht.attrib["arbeitszeit"]
                    berichtB = bericht.text
                    neuerDictEintrag = dict()
                    neuerDictEintrag["arbeitszeit"] = int(arbeitszeitB)
                    neuerDictEintrag["bericht"] = berichtB
                    jsonInhalt[datumB][modulB].append(neuerDictEintrag)

    sortierteZeiten = dict(sorted(jsonInhalt.items()))
    gedumpteVersion = json.dumps(sortierteZeiten)

    with open(f"/home/ubuntu/django-test/newApp/templates/newApp/{keks}.json", "w") as datei2:
        datei2.write(gedumpteVersion)
    os.remove(pfad)
    
def csvUpload(request, dateiName):
    keks = request.COOKIES.get("cookie_username", False)
    jsonInhalt = dict()

    pfad = os.path.join(settings.MEDIA_ROOT, dateiName)

    with open(pfad, "r", newline="", encoding="utf-8") as dateiC:
        reader = csv.reader(dateiC, delimiter="|")
        skipHeader = next(reader)
        for zeile in reader:
            datumB = zeile[0]
            modulB = zeile[1]
            arbeitszeitB = zeile[2]
            berichtB = zeile[3]
            
            if datumB not in jsonInhalt:
                jsonInhalt[datumB] = dict()
            if modulB not in jsonInhalt[datumB]:
                jsonInhalt[datumB][modulB] = list()
                neuerDictEintrag = dict()
                neuerDictEintrag["arbeitszeit"] = int(arbeitszeitB)
                neuerDictEintrag["bericht"] = berichtB
                jsonInhalt[datumB][modulB].append(neuerDictEintrag)

    sortierteZeiten = dict(sorted(jsonInhalt.items()))
    gedumpteVersion = json.dumps(sortierteZeiten)

    with open(f"/home/ubuntu/django-test/newApp/templates/newApp/{keks}.json", "w") as datei2:
        datei2.write(gedumpteVersion)
    os.remove(pfad)

def jsonUpload(request, dateiName):
    keks = request.COOKIES.get("cookie_username", False)

    pfad = os.path.join(settings.MEDIA_ROOT, dateiName)
    with open(pfad, "r", encoding="utf-8") as dateiJ:
        inhalt = dateiJ.read()

    with open(f"/home/ubuntu/django-test/newApp/templates/newApp/{keks}.json", "w") as datei2:
        datei2.write(inhalt)
    
    os.remove(pfad)

def nutzerDatenbankAuslesen():
    with open("/home/ubuntu/django-test/newApp/templates/newApp/nutzerDatenbank.json", "r") as datei:
        dateiLesen = datei.read()
        alleUser = json.loads(dateiLesen)
    return alleUser

def uebersichtVorhandeneUser(request):
    alleUser = nutzerDatenbankAuslesen()

    listeGesperrteUser = list()
    listeAktiveUser = list()
    
    for user in alleUser:
        if user["Sperrung"] == False:
            listeAktiveUser.append(user)
        elif user["Sperrung"] == True:
            listeGesperrteUser.append(user)
    return [listeGesperrteUser, listeAktiveUser]

def userSperren(request, userMail):
    alleUser = nutzerDatenbankAuslesen()
    for user in alleUser:
        if user["Mail"] == userMail:
            user["Sperrung"] = True
    alleUser = json.dumps(alleUser)
    with open("/home/ubuntu/django-test/newApp/templates/newApp/nutzerDatenbank.json", "w") as datei:
        datei.write(alleUser)

def userFreigeben(request, userMail):
    alleUser = nutzerDatenbankAuslesen()
    for user in alleUser:
        if user["Mail"] == userMail:
            user["Sperrung"] = False

    alleUser = json.dumps(alleUser)
    with open("/home/ubuntu/django-test/newApp/templates/newApp/nutzerDatenbank.json", "w") as datei:
        datei.write(alleUser)

def uebersichtModule(request):
    with open("/home/ubuntu/django-test/newApp/templates/newApp/module.json", "r") as dateiM:
        inhalt = dateiM.read()
        alleModule = json.loads(inhalt)

    gesperrteModule = list()
    aktiveModule = list()
    for modul in alleModule:
        if alleModule[modul] == True:
            aktiveModule.append(modul)
        elif alleModule[modul] == False:
            gesperrteModule.append(modul)
    
    return [gesperrteModule, aktiveModule]

def modulFreischalten(request, freizuschaltendesModul):  
    with open("/home/ubuntu/django-test/newApp/templates/newApp/module.json", "r") as dateiM:
        inhalt = dateiM.read()
        alleModule = json.loads(inhalt)
    
    for modul in alleModule:
        if modul == freizuschaltendesModul:
            alleModule[modul] = True
    
    deserialisierteModule = json.dumps(alleModule)
    with open("/home/ubuntu/django-test/newApp/templates/newApp/module.json", "w") as dateiM:
        dateiM.write(deserialisierteModule)

def modulSperren(request, sperrenModul):  
    with open("/home/ubuntu/django-test/newApp/templates/newApp/module.json", "r") as dateiM:
        inhalt = dateiM.read()
        alleModule = json.loads(inhalt)
    
    for modul in alleModule:
        if modul == sperrenModul:
            alleModule[modul] = False
    
    deserialisierteModule = json.dumps(alleModule)
    with open("/home/ubuntu/django-test/newApp/templates/newApp/module.json", "w") as dateiM:
        dateiM.write(deserialisierteModule)

def neuesModul(request, modul):
    with open("/home/ubuntu/django-test/newApp/templates/newApp/module.json", "r") as dateiM:
        inhalt = dateiM.read()
        alleModule = json.loads(inhalt)
    
    alleModule[modul] = True
    
    deserialisierteModule = json.dumps(alleModule)
    with open("/home/ubuntu/django-test/newApp/templates/newApp/module.json", "w") as dateiM:
        dateiM.write(deserialisierteModule)