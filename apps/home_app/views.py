from django.db.models import Q
from django.shortcuts import render
from django.views.generic import View, TemplateView
from .models import SliderBannerImage, FQuestions, AboutUs, BannerSectionOne, BannerSectionTwo, ShippingMethod
from apps.product_app.models import Tag, Product
from apps.blog_app.models import Blog
from django.http import JsonResponse


class Home(View):
    def get(self, request):
        slider_banner_images = SliderBannerImage.objects.filter(status=True).order_by('sort_number').defer('upload_at', 'status')
        blogs = Blog.objects.filter(status=True)[:6].select_related('author')
        products = Product.objects.filter(
            Q(selected_product=True) | Q(remaining_time__isnull=False)
        ).prefetch_related('category', 'tag').defer('description', 'property', 'created_at', 'update_at')
        section_one_banners = BannerSectionOne.objects.all()[:4].defer('upload_at', 'update_at')
        section_two_banner = BannerSectionTwo.objects.last()
        return render(request, 'home_app/home.html', {
            'sliderBannerImages': slider_banner_images,
            'sectionOneBanners': section_one_banners,
            'sectionTwoBanner': section_two_banner,
            'blogs': blogs,
            'products': products
        })


class FrequentlyQuestions(TemplateView):
    template_name = 'home_app/faq.html'

    def get_context_data(self, **kwargs):
        context = super(FrequentlyQuestions, self).get_context_data(**kwargs)
        context['frequently_questions'] = FQuestions.objects.filter(status=True).defer('update_at', 'created_at')
        context['tags'] = Tag.objects.all().defer('created_at')
        return context


class AboutUsView(TemplateView):
    template_name = 'home_app/aboutus.html'

    def get_context_data(self, **kwargs):
        context = super(AboutUsView, self).get_context_data(**kwargs)
        context['aboutUs'] = AboutUs.objects.last()
        context['blogs'] = Blog.objects.filter(status=True)[:6].select_related('author')
        return context


def countdown_end(request):
    if request.method == 'POST':
        try:
            product_id = request.POST.get('productID')
            product = Product.objects.get(id=product_id)
            product.special_price = None
            product.remaining_time = None
            product.save()
            return JsonResponse({'status': 200, 'product_name': product.product_name})
        except:
            return JsonResponse({'status': 400})


class ShippingMethodView(TemplateView):
    template_name = 'templates/includes/shipping-method.html'

    def get_context_data(self, **kwargs):
        context = super(ShippingMethodView, self).get_context_data(**kwargs)
        context['methods'] = ShippingMethod.objects.all().defer('update_at')
        return context
