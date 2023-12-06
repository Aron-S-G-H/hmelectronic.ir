from apps.product_app.models import Product

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get(CART_SESSION_ID)

        if not cart:
            cart = self.session[CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()
        for item in cart.values():
            product = Product.objects.get(id=int(item['product_id']))
            item['product'] = product
            item['total'] = int(item['quantity']) * int(float(item['price']))
            item['unique_id'] = self.unique_id_generator(product.id, item['price'])
            yield item

    def unique_id_generator(self, id, product_price):
        result = f'{id}__{product_price}'
        return result

    def cart_quantity(self):
        cart = self.cart.values()
        quantity = len(cart)
        return quantity

    def total(self):
        cart = self.cart.values()
        total = sum(int(float(item['price'])) * int(item['quantity']) for item in cart)
        return total

    def add(self, product, quantity, tip_price=None):
        if product.special_price:
            unique_id = self.unique_id_generator(product.id, product.special_price)
        else:
            price = tip_price if tip_price else product.price
            unique_id = self.unique_id_generator(product.id, price)
        if unique_id not in self.cart:
            if product.special_price:
                discount_percent = int(((product.price - product.special_price) * 100) / product.price)
                final_price = product.special_price
                self.cart[unique_id] = {
                    'quantity': 0,
                    'price': str(final_price),
                    'product_id': str(product.id),
                    'discount_percent': str(discount_percent),
                }
            else:
                self.cart[unique_id] = {
                    'quantity': 0,
                    'price': str(tip_price) if tip_price else str(product.price),
                    'product_id': str(product.id),
                }
        self.cart[unique_id]['quantity'] += int(quantity)
        self.save()

    def remove_cart(self):
        del self.session[CART_SESSION_ID]

    def delete(self, unique_id):
        if unique_id in self.cart:
            del self.cart[unique_id]
            self.save()

    def save(self):
        self.session.modified = True
