from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('signUp/', views.signUp, name='signUp'),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path('signIn/', views.signIn, name='signIn'),
    path('logout/', views.logout, name='logout'),
    path('myAccount/', views.myAccount, name='myAccount'),
    path('patientDashboard/', views.patientDashboard, name='patientDashboard'),
    path('doctorDashboard/', views.doctorDashboard, name='doctorDashboard'),
]
