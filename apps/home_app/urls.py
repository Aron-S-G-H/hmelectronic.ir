from django.views.decorators.cache import cache_page
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.Home.as_view(), name='Home_Page'),
    path('fq', cache_page(60 * 20)(views.FrequentlyQuestions.as_view()), name='FrequentlyQuestions_Page'),
    path('aboutus', views.AboutUsView.as_view(), name='AboutUs_Page'),
    path('countdown-end', views.countdown_end, name='countdown_end'),
    path('shipping-method', cache_page(60 * 20)(views.ShippingMethodView.as_view()), name='shipping_method'),
]
