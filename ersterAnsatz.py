import json
import csv

class Zeiterfassung:
    alleZeiterfassungen = set()
    def __init__(self):
        self.zeiten = dict()
        """
        self.__zeiten = {
        "10.11.2023": { "Straße gekehrt": "4 Stunden",
                        "Blumenbeete neu angelegt": "2 Stunden"}
        "11.11.2023": { "Park bewässert": "1,5 Stunden",
                        "Einsatz Parkbeleuchtung repariert": "0,5 Stunden"}
        ......
        }
        """
        Zeiterfassung.alleZeiterfassungen.add(self)

class Nutzer:
    alleNutzer = set()
    def __init__(self, rolle, mail, password):
        self.__rolle = rolle
        self.__mail = mail
        self.__password = password
        self.__sperrung = False
        self.zeiterfassung = Zeiterfassung()
        Nutzer.alleNutzer.add(self)

    def sperreKonto(self):
        self.__sperrung = True
        return "Konto erfolgreich gesperrt"

    def neueBuchung(self, tag, stunden, bericht):
        if tag not in self.zeiterfassung.zeiten:                # prüft ob an dem Tag schon gearbeitet wurde, falls nicht:
            self.zeiterfassung.zeiten[tag] = dict()             # erstelle ein neuen Key im Dict und füge ihm als Wert ein Dict hinzu
        self.zeiterfassung.zeiten[tag][bericht] = stunden       # gehe zum Key (Tag) und füge dem Tag die Stunden als Key und den Bericht als Value hinzu

    def speichereNutzerInDieJsonDatei():                        # diese Methode kann der Nutzer nicht ausführen!
        nutzer_liste = []                                       # diese Methode bildet unsere Datenbank
        for nutzer in Nutzer.alleNutzer:
            nutzer_info = {
            "Rolle": nutzer._Nutzer__rolle,
            "Mail": nutzer._Nutzer__mail,
            "Password": nutzer._Nutzer__password,
            "Sperrung": nutzer._Nutzer__sperrung,
            "Zeiterfassung": nutzer.zeiterfassung.zeiten         # hier wird nur die Zeiterfassung gespeichert, nicht das gesamte Objekt (evtl problematisch!)
            }
            nutzer_liste.append(nutzer_info)
        with open("nutzerDatenbank.json", "w") as datei:
            json.dump(nutzer_liste, datei, indent=2)
    
    def jsonDateiMitZeitenDesUsers(userMail):                   # diese Methode kann der User ausführen
        with open("nutzerDatenbank.json", "r") as datei2:
            deserialisierteDatei2 = json.load(datei2)
            for listeneintrag in deserialisierteDatei2:
                if listeneintrag["Mail"] == userMail:
                    with open("zeitenDesUsers.json", "w") as datei3:
                        zeiten = listeneintrag["Zeiterfassung"]
                        serialisierteZeiten = json.dumps(zeiten)
                        datei3.write(serialisierteZeiten)

    def csvDateiMitZeitenDesUsers(userMail):                    # diese Methode kann der User ausführen
        with open("nutzerDatenbank.json", "r") as datei4:
            deserialisierteDatei4 = json.load(datei4)
            for listeneintrag in deserialisierteDatei4:
                if listeneintrag["Mail"] == userMail:
                    with open("zeitenDesUsers.csv", "w", newline="") as datei5:
                        writer = csv.writer(datei5, delimiter=";")
                        for eintrag in listeneintrag["Zeiterfassung"]:
                            eintrag1 = eintrag
                            eintrag2 = dict()
                            for treffer in listeneintrag["Zeiterfassung"][eintrag]:
                                eintrag2[treffer] = listeneintrag["Zeiterfassung"][eintrag][treffer]
                            writer.writerow([eintrag1, eintrag2])



tomMustermann = Nutzer("einfache Anwender", "tom.mustermann@test.de", "pw123")
laraMeier = Nutzer("VIP Anwender", "lara.meier@test.de", "pw456")

tomMustermann.neueBuchung("15.11.2023", "1 Stunde", "Wohnung geputzt")
tomMustermann.neueBuchung("15.11.2023", "4 Stunden", "Gartenarbeit")
tomMustermann.neueBuchung("20.11.2023", "3 Stunden", "Fenster geputzt")

laraMeier.neueBuchung("10.11.2023", "3 Stunden", "Essen gekocht")

Nutzer.speichereNutzerInDieJsonDatei()
Nutzer.jsonDateiMitZeitenDesUsers("tom.mustermann@test.de")
Nutzer.csvDateiMitZeitenDesUsers("tom.mustermann@test.de")