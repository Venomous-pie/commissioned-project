# cart/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem
from django.http import JsonResponse

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
    quantity = int(request.POST.get('quantity', 1))  # Get quantity from form, default to 1
    
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()
    except CartItem.DoesNotExist:
        CartItem.objects.create(cart=cart, product=product, quantity=quantity)
    
    messages.success(request, f"{product.name} added to your cart!")
    
    # If this is AJAX request, return updated cart count as JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_items = cart.items.all()
        cart_count = sum(item.quantity for item in cart_items)
        return JsonResponse({'cart_count': cart_count})
    
    # Check if there's a next parameter to redirect back to the referring page
    next_url = request.GET.get('next')
    if next_url:
        return redirect(next_url)
    
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
        cart_items = cart.items.all()
        count = sum(item.quantity for item in cart_items)
    elif hasattr(request, 'session') and request.session.session_key:
        session_id = request.session.session_key
        cart = Cart.objects.filter(session_id=session_id).first()
        if cart:
            cart_items = cart.items.all()
            count = sum(item.quantity for item in cart_items)
    
    return {'cart_count': count}