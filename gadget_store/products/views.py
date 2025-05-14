# products/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Wishlist
from django.contrib import messages
import random


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
    
    if category_id:
        products = products.filter(category__id=category_id)
    
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None
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
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    
    if created:
        messages.success(request, f"{product.name} added to your wishlist!")
    else:
        messages.info(request, f"{product.name} is already in your wishlist!")
    
    return redirect('product_detail', slug=product.slug)

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