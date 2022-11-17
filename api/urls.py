from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('auth', views.auth),
    path('email', views.email_send),
    path('create', views.createuser),
    path('user',views.user_details),
]
