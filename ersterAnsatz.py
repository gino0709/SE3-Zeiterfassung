import json

class Zeiterfassung:
    alleZeiterfassungen = set()
    def __init__(self, userId):
        self.__userId = userId
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
    def __init__(self, rolle, nutzerId, mail, username, password):
        self.__rolle = rolle
        self.__nutzerId = nutzerId
        self.__mail = mail
        self.__username = username
        self.__password = password
        self.__sperrung = False
        self.zeiterfassung = Zeiterfassung(self.__nutzerId)
        Nutzer.alleNutzer.add(self)

    def sperreKonto(self):
        self.__sperrung = True
        return "Konto erfolgreich gesperrt"

    def neueBuchung(self, tag, stunden, bericht):
        if tag not in self.zeiterfassung.zeiten:                # prüft ob an dem Tag schon gearbeitet wurde, falls nicht:
            self.zeiterfassung.zeiten[tag] = dict()             # erstelle ein neuen Key im Dict und füge ihm als Wert ein Dict hinzu
        self.zeiterfassung.zeiten[tag][stunden] = bericht       # gehe zum Key (Tag) und füge dem Tag die Stunden als Key und den Bericht als Value hinzu

    def speichereNutzerInDieJsonDatei():
        nutzer_liste = []
        for nutzer in Nutzer.alleNutzer:
            nutzer_info = {
            "Rolle": nutzer._Nutzer__rolle,
            "NutzerId": nutzer._Nutzer__nutzerId,
            "Mail": nutzer._Nutzer__mail,
            "Username": nutzer._Nutzer__username,
            "Password": nutzer._Nutzer__password,
            "Sperrung": nutzer._Nutzer__sperrung,
            "Zeiterfassung": nutzer.zeiterfassung.zeiten  # Hier wird nur die Zeiterfassung gespeichert, nicht das gesamte Objekt
        }
        nutzer_liste.append(nutzer_info)

tomMustermann = Nutzer("einfache Anwender", 1001, "tom.mustermann@test.de", "tomM", "pw123")
laraMeier = Nutzer("VIP Anwender", 1002, "lara.meier@test.de", "laraM", "pw456")

tomMustermann.neueBuchung("15.11.2023", "1 Stunde", "Wohnung geputzt")

with open("nutzerDatenbank.json", "w") as datei:
    datei.write(json.dumps(Nutzer.speichereNutzerInDieJsonDatei()))