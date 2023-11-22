"""
Dateienberechtigungen ändern in Python

Allgemeine Einführung:

d = dictionary
- = normale Datei

r = read
w = write
x = execute

Buchstabe 1: Dateityp
Buchstabe 2-4: Berechtigungen Benutzer (user)
Buchstabe 5-7: Berechtigungen Gruppe, die der Benutzer angehört (group)
Buchstabe 8-10: Berechtigungen anderer Benutzer (others)

Bsp. (drwxr-xr-x):
Buchstabe 1: Ein Ordner
Buchstabe 2-4: Benutzer kann lesen, schreiben und ausführen
Buchstabe 5-7: Seine Gruppe kann nur lesen und ausführen
Buchstabe 8-10: Andere Benutzer können ebenfalls nur lesen und ausführen

Berechtigungsbits (mit st_mode kann man die Berechtigungsbits sich anzeigen lassen):
rwx rwx rwx = 111 111 111
rw- rw- rw- = 110 110 110
rwx --- --- = 111 000 000

rwx = 111 in binary = 7
rw- = 110 in binary = 6
r-x = 101 in binary = 5
r-- = 100 in binary = 4

Berechtigungs-Flags/permissionFlag (mit stat kann man den Berechtigungsmodus ändern):
user:
r = stat.S_IREAD
w = stat.S_IWRITE
x = stat.S_IEXEC
r,w,x = stat.S_IRWXU
group:
r = stat.S_IRGRP
w = stat.S_IWGRP
x = stat.S_IXGRP
r,w,x = stat.S_IRWXG
others:
r = stat.S_IROTH
w = stat.S_IWOTH
x = stat.S_IXOTH
r,w,x = stat.S_IRWXO

Berechtigungen im Code ändern:
os.chmod(filePath, permissionFlag)
Bsp.: os.chmod("Test2.txt", stat.S_IWGRP)

Statt Berechtigungsflags kann man auch Oktalzahlen anwenden. 
Bsp.: 755 -> drwxr-xr-x bzw. -rwxr-xr-x
os.chmod("Test2.txt", 0o755)    #0o ist ein Präfix und wird benötigt, um anzuzeigen, dass es sich hier 
                                um eine oktale Notation handelt
"""
import os
import stat
#from django.conf import settings

# Um Berechtigungsmodus herauszufinden:
fileName = "Test.txt"
#filePath = os.path.join(settings.BASE_DIR, fileName)
os.chdir("C:/Users/Schulamith/Desktop/ÜbungTDD/Systeme (Projekt) (3. Semester)/Daran arbeite ich gerade")
perm = os.stat(fileName)             # os.stat() erhält Status eines angegebenen Pfads
print(perm)             
print(perm.st_mode)                     # st_mode stellt Berechtigungsbits der Datei bereit (ersten beiden Oktalziffern 
                                        # geben den Dateityp an und die anderen vier die Dateiberechtigungen) Hier: 33206
os.chmod(fileName, stat.S_IWGRP)     
os.chmod(fileName, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC | stat.S_IRUSR)

perm = os.stat(fileName)             
print(perm.st_mode)    

"""
Möglich wäre es auch, die einzelnen Berechtigungen in Variablen zu speichern und diese anstatt den permissionFlags in den Code zu schreiben.

import os
import stat

def remove_write_permissions(path)
    NO_USER_WRITING = ~stat.S_IWUSR             # ~ ist ein Operator, der alle Bits umdreht; Hier: Schreibrecht vom User war vorher eine 1 und ist jz eine 0 
    NO_GROUP_WRITING = ~stat.S_IWGRP
    NO_OTHER_WRITING = ~stat.S_IWOTH
    NO_WRITING = NO_USER_WRITING & NO_GROUP_WRITING & NO_OTHER_WRITING

    current_permissions = stat.S_IMODE(os.lstat(path)).st_mode) # ruft Berechtigungen der aktuellen Datei auf
    os.chmod(path, current_permissions & NO_WRITING)
"""