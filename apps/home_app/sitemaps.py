from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.templatetags.static import static


class StaticSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return [
            'main:AboutUs_Page',
            'main:Home_page',
            'contactUs:contact_page',
            'account:login',
            'account:register',
            'blog:list',
        ]

    def location(self, item):
        return reverse(item)


class FaviconSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"
    protocol = 'https'

    def items(self):
        return ['image/favicon.png']

    def location(self, item):
        return static(item)
