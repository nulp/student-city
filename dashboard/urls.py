
from django.contrib import admin
from django.urls import path, include
from .views import dashboard_view, logout_view, login_view, pdb_test_view


# app_name = 'dashboard'

urlpatterns = [
    path('', dashboard_view, name="main"),
    path('', dashboard_view, name="add_person"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('populate-db/', pdb_test_view,),
]
