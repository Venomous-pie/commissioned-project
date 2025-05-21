from .models import Category
from products.models import Wishlist

def categories_processor(request):
    categories = Category.objects.all()
    return {'categories': categories}

def wishlist_processor(request):
    """Add a list of product IDs in the user's wishlist to the context"""
    in_wishlist_products = []
    
    if request.user.is_authenticated:
        try:
            wishlist_items = Wishlist.objects.filter(user=request.user)
            in_wishlist_products = [item.product.id for item in wishlist_items]
        except:
            in_wishlist_products = []
    
    return {'in_wishlist_products': in_wishlist_products}
