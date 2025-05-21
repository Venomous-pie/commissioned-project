def cart_count(request):
    from .models import Cart
    
    count = 0
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = sum(item.quantity for item in cart.items.all())
        except Cart.DoesNotExist:
            count = 0
    elif hasattr(request, 'session') and request.session.session_key:
        session_id = request.session.session_key
        try:
            cart = Cart.objects.get(session_id=session_id)
            count = sum(item.quantity for item in cart.items.all())
        except Cart.DoesNotExist:
            count = 0
    
    return {'cart_count': count}

def cart_contents(request):
    cart_items = []
    
    from products.models import Product
    from .models import Cart, CartItem
    
    # Get current cart
    if request.user.is_authenticated:
        try:
            cart_obj = Cart.objects.get(user=request.user)
            cart_items = cart_obj.items.all()
            # Create a list of product IDs in cart for template usage
            in_cart_products = [item.product.id for item in cart_items]
        except Cart.DoesNotExist:
            in_cart_products = []
    elif hasattr(request, 'session') and request.session.session_key:
        session_id = request.session.session_key
        try:
            cart_obj = Cart.objects.get(session_id=session_id)
            cart_items = cart_obj.items.all()
            in_cart_products = [item.product.id for item in cart_items]
        except Cart.DoesNotExist:
            in_cart_products = []
    else:
        in_cart_products = []
        
    return {
        'cart_items': cart_items,
        'in_cart_products': in_cart_products
    }
