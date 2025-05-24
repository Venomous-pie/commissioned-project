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
    name = models.CharField(max_length=1000)
    slug = models.CharField(max_length=1000, unique=True)
    image = models.CharField(max_length=1000)
    description = models.TextField()
    brand = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.FloatField()
    rating = models.FloatField()
    rating_count = models.IntegerField()
    availability_status = models.CharField(max_length=1000)
    stock = models.IntegerField()
    tags = models.CharField(max_length=1000)
    warranty_information = models.TextField()
    shipping_information = models.TextField()
    return_policy = models.TextField()
    sku = models.CharField(max_length=1000)
    weight = models.FloatField()
    dimensions = models.CharField(max_length=1000)
    thumbnail_url = models.CharField(max_length=1000)
    is_featured = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    
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
