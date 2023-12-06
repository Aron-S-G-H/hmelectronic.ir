from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('detail', views.CartDetailView.as_view(), name='detail_page'),
    path('add/<int:pk>', views.CartAddView.as_view(), name='addToCart'),
    path('remove/<str:unique_id>', views.CartRemoveView.as_view(), name='removeFromCart'),
    path('update', views.UpdateCartView.as_view(), name='update-cart'),
    path('checkout', views.CheckOutView.as_view(), name='checkOut_page'),
    path('pdf/invoice/<int:order_id>', views.admin_invoice_pdf, name='admin_invoice_page')
]
