from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from Electronic import settings
from apps.product_app.api import ProductApi
from apps.product_app.sitemaps import ProductSiteMap
from apps.blog_app.sitemaps import BlogSiteMap
from apps.home_app.sitemaps import StaticSiteMap, FaviconSitemap
from .views import robots
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'products': ProductSiteMap,
    'blogs': BlogSiteMap,
    'static': StaticSiteMap,
    "favicon": FaviconSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.home_app.urls')),
    path('contact-us/', include('apps.contact_app.urls')),
    path('shop/', include('apps.product_app.urls')),
    path('api/torob/products/', ProductApi.as_view(), name='product_api'),
    path('api/torob/products', ProductApi.as_view(), name='product_api'),
    path('blog/', include('apps.blog_app.urls')),
    path('account/', include('apps.account_app.urls')),
    path('cart/', include('apps.cart_app.urls')),
    path('payment-gateway/', include('apps.zarinpal_app.urls')),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path('robots.txt', robots, name="robots"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = "Electronic.views.page_not_found_view"
