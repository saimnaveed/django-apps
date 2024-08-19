from django.contrib import admin
from django.urls import path, include
from authwork import views

urlpatterns = [
    path('', views.index, name="authwork"),
    path('login', views.login_user, name="login"),
    path('logout', views.logout_user, name="logout"),
]