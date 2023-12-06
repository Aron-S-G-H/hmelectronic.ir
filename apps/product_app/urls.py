from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('', views.Shop.as_view(), name='shop_page'),
    path('product/<int:pk>/<str:slug>', views.ProductDetailView.as_view(), name='productDetail_page'),
    path('categoryPartial/<str:slug>', views.CategoryPartialView.as_view(), name='categoryPartial'),
    path('mobileCategoryPartial/<str:slug>', views.MobileCategoryPartialView.as_view(), name='mobileCategoryPartial'),
    path('category-details/<int:pk>/<str:slug>', views.CategoryDetailView.as_view(), name='categoryDetails_page'),
    path('reizan-info/<str:slug>', views.show_tip_reizan, name='show_reizan_tip'),
]
