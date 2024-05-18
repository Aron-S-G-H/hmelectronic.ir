from django.views.decorators.cache import cache_page
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.Home.as_view(), name='Home_page'),
    path('aboutus', cache_page(60 * 30)(views.AboutUsView.as_view()), name='AboutUs_Page'),
    path('countdown-end', views.countdown_end, name='countdown_end'),
]
