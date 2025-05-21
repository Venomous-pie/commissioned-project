# products/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Wishlist
from django.contrib import messages
import random
from django.db import models
from django.http import JsonResponse


def home(request):
    products = list(Product.objects.all())
    random.shuffle(products)
    featured_products = products[:8]  # get 8 random products

    categories = Category.objects.all()

    return render(request, 'products/home.html', {
        'featured_products': featured_products,
        'categories': categories
    })

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    search_query = request.GET.get('q')
    sort = request.GET.get('sort', 'featured')
    
    # Apply search filter
    if search_query:
        products = products.filter(
            models.Q(name__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(tags__icontains=search_query) |
            models.Q(brand__icontains=search_query)
        )
    
    # Apply category filter
    if category_id:
        products = products.filter(category__id=category_id)
    
    # Apply sorting
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created')
    elif sort == 'rating':
        products = products.order_by('-rating')
    else:  # featured
        products = products.order_by('-is_featured', '-created')
    
    # Get total products count for the sidebar
    total_products = Product.objects.count()
    
    # Add product count to categories
    for category in categories:
        category.product_count = Product.objects.filter(category=category).count()
    
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'total_products': total_products
    })

def product_detail(request, slug):
    # Get the product
    product = get_object_or_404(Product, slug=slug)
    
    # Get related products (same category)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    
    return render(request, 'products/product_detail.html', context)

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': category.id
    })

@login_required
def add_to_wishlist(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
        
        if created:
            status_message = f"{product.name} added to your wishlist!"
            in_wishlist = True
            messages.success(request, status_message)
        else:
            # If it already exists, remove it (toggle behavior)
            wishlist_item.delete()
            status_message = f"{product.name} removed from your wishlist!"
            in_wishlist = False
            messages.info(request, status_message)
        
        # Get updated wishlist count
        wishlist_count = Wishlist.objects.filter(user=request.user).count()
        
        # If this is an AJAX request, return JSON response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': status_message,
                'in_wishlist': in_wishlist,
                'wishlist_count': wishlist_count
            })
        
        # For non-AJAX requests, redirect to the referring page if possible
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        
        return redirect('product_detail', slug=product.slug)
    
    except Exception as e:
        # Log the error (in production, use a proper logger)
        print(f"Error in add_to_wishlist: {e}")
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': "An error occurred. Please try again.",
            }, status=500)
            
        messages.error(request, "An error occurred. Please try again.")
        return redirect('product_list')

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    messages.success(request, f"{product.name} removed from your wishlist!")
    
    return redirect('wishlist')

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'products/wishlist.html', {'wishlist_items': wishlist_items})

def search_suggestions(request):
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'suggestions': []})
    
    products = Product.objects.filter(
        models.Q(name__icontains=query) |
        models.Q(description__icontains=query) |
        models.Q(tags__icontains=query) |
        models.Q(brand__icontains=query)
    )[:5]  # Limit to 5 suggestions
    
    suggestions = []
    for product in products:
        suggestions.append({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'image_url': product.image.url if product.image else '',
            'category': product.category.name,
            'url': product.get_absolute_url()
        })
    
    return JsonResponse({'suggestions': suggestions})