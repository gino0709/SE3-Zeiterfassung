from django.urls import path
from newApp import views


urlpatterns = [
    path("Unterseite/", views.home),
    path("Startseite/", views.startseite),
    path("test/", views.getBaseDir),
    path("registratur", views.registratur),
    path("downloads.csv", views.jsonInCsv),
    path("downloads.json", views.jsonDownload),
    path("downloads.xml", views.jsonInXml),
    ]