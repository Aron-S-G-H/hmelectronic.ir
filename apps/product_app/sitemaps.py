from django.contrib.sitemaps import Sitemap
from .models import Product


class ProductSiteMap(Sitemap):
    changefreq = "daily"
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Product.objects.all()

    def lastmod_field(self, obj):
        return obj.update_at

    def location(self, item):
        return item.get_absolute_url()
