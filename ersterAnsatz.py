import json

class Zeiterfassung:
    alleZeiterfassungen = set()
    def __init__(self):
        self.zeiten = dict()
        """
        self.__zeiten = {
        "10.11.2023": { "4 Stunden": "Straße gekehrt, Mülleimer geleert",
                        "2 Stunden": "Blumenbeete neu angelegt"}
        "11.11.2023": { "1,5 Stunden": "Park bewässert",
                        "3 Stunden": "Einsatz Parkbeleuchtung repariert"}
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

    def speichereNutzerInDieJsonDatei():
        nutzer_liste = []
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

tomMustermann = Nutzer("einfache Anwender", "tom.mustermann@test.de", "pw123")
laraMeier = Nutzer("VIP Anwender", "lara.meier@test.de", "pw456")

tomMustermann.neueBuchung("15.11.2023", "1 Stunde", "Wohnung geputzt")
laraMeier.neueBuchung("10.11.2023", "3 Stunden", "Essen gekocht")

Nutzer.speichereNutzerInDieJsonDatei()