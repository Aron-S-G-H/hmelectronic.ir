from django.shortcuts import render
from apps.product_app.models import Tag
from django.views.generic import View, TemplateView
from .models import Blog, Comment
from django.http import JsonResponse
from hitcount.views import HitCountDetailView
from django.core.paginator import Paginator
from django.contrib import messages


class BlogListView(View):
    def get(self, request):
        blogs = Blog.objects.filter(status=True).select_related('author')
        if not blogs:
            messages.info(request, 'مقاله ای در سایت انتشار نیافته است !')
            return render(request, 'blog_app/blogs-list.html')
        page_number = request.GET.get('page')
        paginator = Paginator(blogs, 6)
        blogs_list = paginator.get_page(page_number)
        return render(request, 'blog_app/blogs-list.html', {'blogs_list': blogs_list})


class BlogSideBarPartial(TemplateView):
    template_name = 'blog_app/blog-sideBar.html'

    def get_context_data(self, **kwargs):
        context = super(BlogSideBarPartial, self).get_context_data(**kwargs)
        context['product_tags'] = Tag.objects.all().defer('created_at')
        return context


class BlogDetailView(HitCountDetailView):
    model = Blog
    context_object_name = 'blog'
    template_name = 'blog_app/blog-detail.html'
    slug_field = 'slug'
    count_hit = True

    # Post Method is for Creating Comments
    def post(self, request, slug):
        if request.user.is_authenticated:
            text = request.POST.get('text')
            parent_id = request.POST.get('parent_id')
            try:
                blog = Blog.objects.get(slug=slug)
                Comment.objects.create(blog=blog, parent_id=parent_id, user=request.user, text=text)
            except:
                return JsonResponse({'status': 400})
            return JsonResponse({'status': 200})
        else:
            return JsonResponse({'status': 401})
