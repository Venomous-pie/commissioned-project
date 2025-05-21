from .models import Category
from products.models import Wishlist
from django.db.models import ObjectDoesNotExist

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
        except ObjectDoesNotExist:
            # This shouldn't happen with filter(), but just in case
            in_wishlist_products = []
        except Exception as e:
            # Log the error (in production you'd use a proper logger)
            print(f"Error in wishlist_processor: {e}")
            in_wishlist_products = []
    
    return {'in_wishlist_products': in_wishlist_products}
