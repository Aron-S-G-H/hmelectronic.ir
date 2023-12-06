from rest_framework import serializers
from .models import Product, ProductImage
from collections import OrderedDict


class ProductSerializer(serializers.ModelSerializer):
    """
    This API was created for Torob.com
    """
    image_links = serializers.SerializerMethodField(source='images')
    title = serializers.CharField(source='product_name')
    image_link = serializers.SerializerMethodField()
    page_unique = serializers.CharField(source='id')
    current_price = serializers.SerializerMethodField()
    old_price = serializers.SerializerMethodField()
    availability = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()
    page_url = serializers.SerializerMethodField()

    def to_representation(self, instance):
        # this function will remove keys that have None value
        result = super(ProductSerializer, self).to_representation(instance)
        return OrderedDict([(key, result[key]) for key in result if result[key] is not None])

    class Meta:
        model = Product
        fields = [
            'title', 'subtitle', 'page_unique', 'current_price', 'old_price',
            'availability', 'category_name', 'image_link', 'image_links', 'page_url'
        ]

    def get_image_link(self, obj):
        request = self.context.get('request')
        image = obj.images.first()
        return request.build_absolute_uri(image.img.url)

    def get_image_links(self, obj):
        request = self.context.get('request')
        images = obj.images.all()
        images_url = []
        for image in images:
            absolute_url = request.build_absolute_uri(image.img.url)
            images_url.append(absolute_url)
        return images_url

    def get_current_price(self, obj):
        if obj.special_price:
            current_price = obj.special_price
        else:
            current_price = obj.price
        return current_price

    def get_old_price(self, obj):
        if obj.special_price:
            old_price = obj.price
            return old_price
        return None

    def get_availability(self, obj):
        if obj.status:
            availability = 'instock'
        else:
            availability = 'outofstock'
        return availability

    def get_category_name(self, obj):
        category = obj.category.first()
        category_name = category.title
        return category_name

    def get_page_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url())
