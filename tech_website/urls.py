from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('about/', views.about, name='about'),
    path('programs/', views.programs, name='programs'),
    path('technology/', views.technology, name='technology'),
    path('technology-transfer/', views.technology_transfer, name='technology_transfer'), 
    path('ipmanagement/', views.ipmanagement, name='ipmanagement'),
    path('spinoff-support/', views.spinoff_support, name='spinoff_support'),
    path('seedgrant/', views.seedgrant, name='seedgrant'),
    path('trl-assessment/', views.trl_assessment, name='trl_assessment'),  
    path('contact/', views.contact, name='contactus'),
    path('services/', views.services, name='services'),  
    path('tech-showcase/', views.tech_showcase, name='tech_showcase'),
]