from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from apps.product_app.models import Product
from .cart_module import Cart
from .forms import CheckoutForm
from .models import UserOrder, ProductOrder
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint
from django.http import HttpResponse, JsonResponse
import json
from django.urls import reverse


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart_app/cart-detail.html', {'cart': cart})


class CartAddView(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        cart = Cart(request)
        quantity = 1
        cart.add(product, quantity)
        return redirect('cart:detail_page')

    def post(self, request, pk):
        quantity = request.POST.get('quantity')
        product_tip = request.POST.get('tip', None)
        try:
            product = Product.objects.get(id=pk)
        except:
            return JsonResponse({'status': 404})
        cart = Cart(request)
        if product_tip == 'A':
            price = product.tipA.first().price
            cart.add(product, quantity, price)
        else:
            cart.add(product, quantity)
        return JsonResponse({'status': 200})


class CartRemoveView(View):
    def get(self, request, unique_id):
        cart = Cart(request)
        cart.delete(unique_id)
        return JsonResponse({'status': 200})


class UpdateCartView(View):
    def post(self, request):
        update_quantity_list = request.POST.get('data')
        update_quantity_list = json.loads(update_quantity_list)
        cart = Cart(request)
        for unique_id in update_quantity_list:
            if unique_id in cart.cart:
                product = cart.cart[unique_id]
                product['quantity'] = int(update_quantity_list[unique_id])
        cart.save()
        return JsonResponse({'status': 200})


class CheckOutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart = Cart(request)
            if cart.cart_quantity() == 0:
                return redirect('cart:detail_page')
            form = CheckoutForm(initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'phone': f'0{request.user.phone}',
                }
            )
            return render(request, 'cart_app/checkout.html', {'form': form})
        else:
            return redirect('account:login')

    def post(self, request):
        cart = Cart(request)
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_order = UserOrder.objects.create(
                user=request.user,
                total_price=cart.total(),
                first_name=cd['first_name'],
                last_name=cd['last_name'],
                email=cd['email'],
                phone=cd['phone'],
                state=cd['state'],
                city=cd['city'],
                postal_code=cd['postal_code'],
                national_code=cd['national_code'],
                address=cd['address'],
                note=cd['note'],
            )
            for item in cart:
                ProductOrder.objects.create(
                    order=new_order,
                    product=item['product'],
                    product_uniqueID=item['unique_id'],
                    product_price=item['price'],
                    quantity=item['quantity'],
                    item_total=item['total'],
                )
            cart.remove_cart()
            request.session['user_order'] = new_order.id
            return redirect(reverse('zarinpal:request'))
        return render(request, 'cart_app/checkout.html', {'form': form})


# Function to output the invoice for each User Order
@staff_member_required
def admin_invoice_pdf(request, order_id):
    order = get_object_or_404(UserOrder, id=order_id)
    html = render_to_string('cart_app/invoice_pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'FileName = order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response)
    return response
