from django.views.decorators.cache import cache_page
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', cache_page(60 * 20)(views.BlogListView.as_view()), name='list'),
    path('detail/<str:slug>', views.BlogDetailView.as_view(), name='detail'),
    path('blog-sidebar', cache_page(60 * 20)(views.BlogSideBarPartial.as_view()), name='blog-sideBarPartial'),
]
