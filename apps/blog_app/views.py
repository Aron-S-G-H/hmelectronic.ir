from django.shortcuts import render
from django.views.generic import View
from .models import Blog, Comment
from django.http import JsonResponse
from hitcount.views import HitCountDetailView
from django.core.paginator import Paginator


class BlogListView(View):
    def get(self, request):
        blogs = Blog.objects.filter(status=True).select_related('author')
        page_number = request.GET.get('page')
        paginator = Paginator(blogs, 12)
        blogs_list = paginator.get_page(page_number)
        return render(request, 'blog_app/blogs-list.html', {'blogs_list': blogs_list})


class BlogSideBarPartial(View):
    def get(self, request, pk):
        recent_blogs = Blog.objects.exclude(id=pk).filter(status=True).select_related('author')[:10]
        return render(request, 'blog_app/blog-sideBar.html', {'recent_blogs': recent_blogs})


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
