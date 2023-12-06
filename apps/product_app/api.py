from .serializers import ProductSerializer
from rest_framework.views import APIView
from .pagination import CustomPagination
from.models import Product


class ProductApi(APIView):
    def post(self, request):
        page_unique = request.data.get('page_unique', None)
        page_url = request.data.get('page_url', None)
        if page_unique:
            page_unique = request.data.get('page_unique', None)
            products = Product.objects.filter(id=page_unique)
        elif page_url:
            product_id = page_url.split('/')[-2]
            product_id = int(product_id)
            products = Product.objects.filter(id=product_id)
        else:
            products = Product.objects.all().order_by('-update_at').prefetch_related('category', 'tag')
        paginator = CustomPagination()
        result = paginator.paginate_queryset(queryset=products, request=request)
        serializer = ProductSerializer(instance=result, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
