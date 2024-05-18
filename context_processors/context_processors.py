from apps.home_app.models import Logo, CommunicationWays, AboutUs, FixedBoxText
from apps.cart_app.cart_module import Cart
from apps.product_app.models import BaseCategory


def data_to_base(request):
    logo = Logo.objects.filter(status=True).last()
    communication_ways = CommunicationWays.objects.last()
    about_us = AboutUs.objects.last()
    cart = Cart(request)
    base_categories = BaseCategory.objects.all()
    fixed_text = FixedBoxText.objects.last()
    return {'logo': logo,
            'communication_ways': communication_ways,
            'aboutUs': about_us,
            'cart': cart,
            'base_categories': base_categories,
            'fixedText': fixed_text}
