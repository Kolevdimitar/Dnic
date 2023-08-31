from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from .models import Cart, CartItem, OrderItem, Order, Product


def landing_page(request):
    return render(request,'shop/landing-page.html')

def product_list(request):
    products = Product.objects.all()

    # Get the cart from the session
    cart = request.session.get('cart', {})

    cart_items = {}
    total_price = 0

    # Populate cart_items dictionary and calculate total price
    for product_id, cart_item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        cart_items[product] = {
            'quantity': cart_item['quantity'],
            'price': cart_item['price'],
        }
        total_price += cart_item['price'] * cart_item['quantity']

    context = {
        'products': products,
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'shop/productlist.html', context)


def product_details(request):
    context = {}
    return render(request,'shop/product-details',context)

def menu_page(request):
    context = {}
    return render(request,'shop/menu-page.html',context)

def shopping_cart(request):
    context = {}
    return render(request,'shop/shopping-cart.html',context)

def checkout_page(request):
    context ={}
    return render(request,'shop/checkout.html',context)

def payment_page(request):
    context ={}
    return render(request,'shop/payment.html',context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', {})

    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
        }

    request.session['cart'] = cart

    return redirect('product-list')


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, pk=cart_item_id)
    cart_item.delete()
    return redirect('cart_view')


def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)
    order = Order.objects.create(order_id="some_unique_id")  # You can generate a unique order_id
    for cart_item in cart.cartitem_set.all():
        OrderItem.objects.create(product=cart_item.product, order=order, order_quantity=cart_item.quantity)
    cart.cartitem_set.all().delete()  # Clear the cart after creating an order
    return render(request, 'shop/checkout.html', {'order': order})

def shopping_cart(request):
    # Assume you have a Cart model that stores cart items and their quantities
    # Replace Cart with your actual model name and adjust the fields accordingly
    cart_items = Cart.objects.all()

    total_price = 0
    for item in cart_items:
        total_price += item.product.price * item.quantity

    context = {
        'cart_items': cart_items,
        'total_price': total_price
    }

    return render(request, 'shop/productlist.html', context)
