from django.contrib.sitemaps import Sitemap
from .models import Blog


class BlogSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.7
    protocol = 'https'

    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.update_at

    def location(self, item):
        return item.get_absolute_url()

