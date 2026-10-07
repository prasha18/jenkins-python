# urls.py

from django.urls import path
from . import views

app_name = 'techforms'

urlpatterns = [
    path('innovation-voucherform/', views.innovation_voucherform, name='innovation_voucherform'),
    path('patent-application/', views.patent_application_form, name='patent_application_form'),
    path('prior-art-search/', views.prior_art_search_form, name='prior_art_search_form'),
    path('trademark-application/', views.trademark_application_form, name='trademark_application_form'),
    path('trl-assessment-form/', views.trl_assessment_form, name='trl_assessment_form'),  
    path('express-interest/', views.express_interest, name='express_interest'),
    path('trademarkapplication/export-data/', views.trademarkapplication_export_data, name='trademarkapplication_export_data'),
    path('priorartapplication/export-data/', views.prior_art_search_export_data, name='prior-art-searchapplication_export_data'),
    path('patentapplication/export-data/', views.patentapplication_export_data, name='patentapplication_export_data'),
    path('innovationapplication/export-data/', views.innovationapplication_export_data, name='innovationapplication_export_data'),
    path('patent/', views.patent, name='patent'),
]