# cart/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem

def _get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    
    return cart

def cart_detail(request):
    cart = _get_cart(request)
    cart_items = cart.items.all()
    total = cart.get_total_price()
    
    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total': total
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)
    
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(cart=cart, product=product)
    
    messages.success(request, f"{product.name} added to your cart!")
    return redirect('cart_detail')

def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart_detail')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, "Item removed from cart!")
    
    return redirect('cart_detail')

# Context processor for cart count
def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        count = cart.items.count()
    elif hasattr(request, 'session') and request.session.session_key:
        session_id = request.session.session_key
        cart = Cart.objects.filter(session_id=session_id).first()
        if cart:
            count = cart.items.count()
    
    return {'cart_count': count}