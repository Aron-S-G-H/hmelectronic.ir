from django.db.models import Q
from django.shortcuts import render
from django.http import Http404
from django.views.generic import View
from .models import Product, Comment, Category, Tag
from django.http import JsonResponse
from django.core.paginator import Paginator
from hitcount.views import HitCountDetailView
from jalali_date import datetime2jalali
from django.contrib.humanize.templatetags.humanize import intcomma
import random


class Shop(View):
    def get(self, request):
        tag_slug = request.GET.get('tag', None)
        max_price = request.GET.get('max_price', None)
        min_price = request.GET.get('min_price', None)
        if tag_slug:
            products = Product.objects.filter(
                tag__slug=tag_slug
            ).prefetch_related('category', 'tag').defer('description', 'property', 'created_at', 'update_at')
        else:
            products = Product.objects.filter(
                Q(selected_product=True) | Q(remaining_time__isnull=False)
            ).prefetch_related('category', 'tag').defer('description', 'property', 'created_at', 'update_at')
        if max_price and min_price:
            products = products.filter(price__gte=int(min_price), price__lt=int(max_price))

        tags = Tag.objects.all().defer('created_at')
        page_number = request.GET.get('page')
        paginator = Paginator(products, 1)
        products_list = paginator.get_page(page_number)
        context = {'products_list': products_list, 'tags': tags}
        if tag_slug:
            context['meta_description'] = f'لیست محصولاتی که دارای برچسب یا تگ {tag_slug} هستند در اچ ام الکترونیک با بهترین کیفیت و ضمانت اصالت کالا'
            context['meta_url'] = f'shop/?tag={tag_slug}'
            context['current'] = f'محصولات دارای تگ {tag_slug}'
        else:
            context['meta_description'] = 'لیست محصولات برگزیده و تخفیف خورده اچ ام الکترونیک صرفه جویی در هزینه و کیفیت بالا'
            context['meta_url'] = 'shop/'
            context['current'] = 'محصولات برگزیده و تخفیف خورده'
        return render(request, 'product_app/shop.html', context)

    def post(self, request):
        search_query = request.POST.get('search', None)
        products = Product.objects.filter(
            product_name__icontains=search_query
        ).prefetch_related('category', 'tag').defer('description', 'property', 'created_at', 'update_at')
        tags = Tag.objects.all().defer('created_at')
        if not products:
            return render(request, 'product_app/shop.html', {'tags': tags, 'current': f'جست و جوی برای {search_query}'})
        page_number = request.GET.get('page')
        paginator = Paginator(products, 12)
        products_list = paginator.get_page(page_number)
        context = {
            'products_list': products_list,
            'tags': tags,
            'current': f'جست و جوی برای {search_query}',
        }
        return render(request, 'product_app/shop.html', context)


class CategoryPartialView(View):
    def get(self, request, slug):
        categories = Category.objects.filter(base_category__slug=slug).select_related('base_category', 'parent')
        return render(request, 'templates/includes/category.html', {'categories': categories})


class MobileCategoryPartialView(View):
    def get(self, request, slug):
        categories = Category.objects.filter(base_category__slug=slug).select_related('base_category', 'parent')
        return render(request, 'templates/includes/mobile-category.html', {'categories': categories})


class ProductDetailView(HitCountDetailView):
    model = Product
    template_name = 'product_app/product-details.html'
    context_object_name = 'product'
    slug_field = 'slug'
    count_hit = True

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = Product.objects.get(id=self.kwargs['pk'], slug=self.kwargs['slug'])
        product_tag = product.tag.first()
        list_similar_products = list(Product.objects.filter(tag__slug=product_tag.slug, status=True).exclude(id=self.kwargs['pk']).prefetch_related('category', 'tag'))
        len_list = len(list_similar_products)
        num_similar_products = 8 if len_list > 8 else len_list
        random_products = random.sample(list_similar_products, k=num_similar_products)
        context['similar_products'] = random_products
        return context

    def post(self, request, pk, slug):
        if request.user.is_authenticated:
            product = Product.objects.get(id=pk, slug=slug)
            text = request.POST.get('text')
            user_name = f'{request.user.first_name} {request.user.last_name}'
            try:
                new_object = Comment.objects.create(user=request.user, product=product, text=text)
                created_date = datetime2jalali(new_object.created_at).strftime('%Y/%m/%d')
            except:
                return JsonResponse({'status': 400})
            return JsonResponse({'status': 200, 'name': user_name, 'created_date': created_date})
        else:
            return JsonResponse({'status': 401})


class CategoryDetailView(View):
    def get(self, request, slug, pk):
        max_price = request.GET.get('max_price', None)
        min_price = request.GET.get('min_price', None)
        try:
            category = Category.objects.get(slug=slug, id=pk)
            if not category.parent:
                products = Product.objects.filter(category__parent=category).prefetch_related('category', 'tag').defer('description', 'property', 'created_at', 'update_at')
            else:
                products = category.products.all()
        except Category.DoesNotExist:
            raise Http404

        if max_price and min_price:
            products = products.filter(price__gte=int(min_price), price__lt=int(max_price))

        tags = Tag.objects.all().defer('created_at')
        if not products:
            return render(request, 'product_app/shop.html', {'tags': tags, 'current': category.title})
        page_number = request.GET.get('page')
        paginator = Paginator(products, 12)
        products_list = paginator.get_page(page_number)
        context = {
            'products_list': products_list,
            'tags': tags,
            'meta_description': 'در این دسته بندی مجموعه متنوع ما از تجهیزات الکترونیکی با کیفیت بالا را مرور کنید',
            'meta_url': f'shop/category-details/{pk}/{slug}',
            'current': category.title,
        }
        return render(request, 'product_app/shop.html', context)


def show_tip_reizan(request, slug):
    if request.method == 'POST':
        tip = request.POST.get('tip')
        if tip:
            try:
                product = Product.objects.get(slug=slug)
                if tip == 'A':
                    tip_a = product.tipA.first()
                    price = intcomma(tip_a.price, use_l10n=False)
                else:
                    price = intcomma(product.price, use_l10n=False)
                return JsonResponse({'status': 200, 'price': price})
            except Product.DoesNotExist:
                return JsonResponse({'status': 404})
        else:
            return JsonResponse({'status': 400})
