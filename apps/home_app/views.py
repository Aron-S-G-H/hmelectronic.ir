import logging
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View, TemplateView
from .models import SliderBannerImage, BannerSectionOne, SliderLogo
from apps.product_app.models import Product, Category
from apps.blog_app.models import Blog
from django.http import JsonResponse
import random


class Home(View):
    def get(self, request):
        slider_banner_images = SliderBannerImage.objects.filter(status=True).order_by('sort_number').defer('created_at', 'update_at')
        companies_logo = SliderLogo.objects.all()[:6]
        categories = []
        for category in Category.objects.all().select_related('base_category', 'parent'):
            if category.has_icon():
                categories.append(category)
        blogs = Blog.objects.filter(status=True)[:8].select_related('author')
        products = Product.objects.filter(
            Q(selected_product=True) | Q(remaining_time__isnull=False)
        ).prefetch_related('category', 'tag').defer('description', 'property', 'created_at', 'update_at')
        section_one_banners = BannerSectionOne.objects.all()[:4].defer('created_at', 'update_at')
        list_backpacks = list(Product.objects.filter(
            tag__slug="کوله-پشتی", status=True
        ).prefetch_related('category', 'tag').defer('description', 'property', 'created_at', 'update_at'))
        random_backpacks = random.sample(list_backpacks, k=8)
        context = {
            'sliderBannerImages': slider_banner_images,
            'companiesLogo': companies_logo,
            'categories': categories,
            'sectionOneBanners': section_one_banners,
            'blogs': blogs,
            'products': products,
            'backpacks': random_backpacks,
        }
        return render(request, 'home_app/home.html', context)


class AboutUsView(TemplateView):
    template_name = 'home_app/aboutus.html'


def countdown_end(request):
    if request.method == 'GET':
        try:
            product_id = request.GET.get('productID')
            product = Product.objects.get(id=product_id)
            product.special_price = None
            product.remaining_time = None
            product.save()
            return JsonResponse({'status': 200, 'product_name': product.product_name})
        except Exception as e:
            logging.warning(f'COUNT-DOWN ERROR: {e}')
            return JsonResponse({'status': 400})
