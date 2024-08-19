
from django.contrib import admin
from django.urls import path
from first_mango import views
urlpatterns = [
    path("", views.index, name='first_mango'),
    path("about", views.about, name='about'),
    path("services", views.services, name='services'),
    path("contacts", views.contacts, name='contacts'),
    path("groupinformatics", views.groupinformatics, name='groupinformatics'),
    path("datascience", views.datascience, name='datascience'),
    path("blockchain", views.blockchain, name='blockchain'),
    path("infrastructure_security", views.infrastructure_security, name='infrastructure_security')
]