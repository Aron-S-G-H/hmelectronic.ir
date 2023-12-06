from django.urls import path
from .views import ContactUsView


app_name = 'contactUs'

urlpatterns = [
    path('', ContactUsView.as_view(), name='contact_page')
]
