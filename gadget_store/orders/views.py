# orders/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from .forms import OrderForm
from cart.views import _get_cart

@login_required
def checkout(request):
    cart = _get_cart(request)
    cart_items = cart.items.all()
    
    if not cart_items:
        messages.warning(request, "Your cart is empty!")
        return redirect('cart_detail')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity
                )
            
            # Clear the cart
            cart_items.delete()
            
            messages.success(request, "Your order has been placed successfully!")
            return redirect('order_complete', order_id=order.id)
    else:
        # Pre-fill form with user profile data if available
        initial_data = {}
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'address': profile.address,
                'city': profile.city,
                'state': profile.state,
                'zip_code': profile.zip_code,
            }
        form = OrderForm(initial=initial_data)
    
    total = cart.get_total_price()
    
    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total': total
    })

@login_required
def order_complete(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'orders/order_complete.html', {'order': order})

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_history.html', {'orders': orders})