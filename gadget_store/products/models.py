# products/models.py

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_products', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=500, unique=True)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    brand = models.CharField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.FloatField(default=0.0)
    rating = models.FloatField(default=0.0)
    rating_count = models.PositiveIntegerField(default=0)
    availability_status = models.CharField(max_length=500, blank=True)
    stock = models.PositiveIntegerField(default=1)
    tags = models.CharField(max_length=500, blank=True)
    warranty_information = models.TextField(blank=True)
    shipping_information = models.TextField(blank=True)
    return_policy = models.TextField(blank=True)
    sku = models.CharField(max_length=500, blank=True)
    weight = models.FloatField(default=0.0)
    dimensions = models.CharField(max_length=500, blank=True)
    thumbnail_url = models.URLField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'product')
    
    def __str__(self):
        return f"{self.user.username}'s wishlist item: {self.product.name}"
