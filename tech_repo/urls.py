from django.urls import path
from .views import get_districts

urlpatterns = [
    path('get_districts/<int:state_id>/', get_districts, name='get_districts'),
]