from django.urls import path
from . import views

app_name = 'zarinpal'

urlpatterns = [
    path('verify/', views.verify, name='verify'),
]
