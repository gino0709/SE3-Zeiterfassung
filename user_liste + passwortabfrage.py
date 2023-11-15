user_login = [
    {"username": "jan_scheffelmeier",
     "mail_adresse": "jan_scheffelmeier@hvf.de",
     "passwort": "JanScheffelmeier"
    },
    {"username": "robin_hospotzky",
     "mail_adresse": "robin_hospotzky@hvf.de",
     "passwort": "RobinHospotzky"
    },
    {"username": "lucia_eiffler",
     "mail_adresse": "lucia_eiffler@hvf.de",
     "passwort": "LuciaEiffler"
    }
]

name = input("Bitte Benutzernamen oder Mail-Adresse eingeben: ")
pw = input("Bitte Passwort eingeben: ")
antwort = False

for user in user_login:
    for data in user:
        if antwort == True:
            break
        elif data == "username":
            if user[data] == name:
                 for data in user:
                    if data == "passwort":
                        if user[data] == pw:
                            antwort = True
                            break
                        else:
                            antwort = False
        elif data == "mail_adresse":
            if user[data] == name:
                for data in user:
                    if data == "passwort":
                        if user[data] == pw:
                            antwort = True
                            break
                        else:
                            antwort = False
        else:
            antwort = False

if antwort == False:
    print("Benutzername / Mail-Adresse oder Passwort falsch!")
elif antwort == True:
    print("Ihr Passwort wurde akzeptiert! \nHerzlich Willkommen '" + name + "'!")