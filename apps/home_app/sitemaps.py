from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = 'https'

    def items(self):
        return [
            'main:AboutUs_Page',
            'main:FrequentlyQuestions_Page',
            'main:Home_Page',
            'contactUs:contact_page',
            'account:login',
            'account:register',
            'blog:list',
        ]

    def location(self, item):
        return reverse(item)
