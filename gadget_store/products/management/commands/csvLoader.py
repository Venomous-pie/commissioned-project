import csv
import os
from django.core.management.base import BaseCommand
from products.models import Product, Category
from django.utils.text import slugify
from django.conf import settings
from django.core.files.base import ContentFile
import requests
from io import BytesIO

class Command(BaseCommand):
    help = 'Load products from a CSV file located in project root'

    def handle(self, *args, **kwargs):
        file_path = os.path.join(settings.BASE_DIR, 'products.csv')
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR('CSV file not found.'))
            return

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category_name = row.get('category', 'Uncategorized')
                category, _ = Category.objects.get_or_create(name=category_name, slug=slugify(category_name))
                
                product_slug = slugify(row['title'])

                # Check if product with this slug already exists
                if Product.objects.filter(slug=product_slug).exists():
                    self.stdout.write(self.style.WARNING(f"Product '{row['title']}' already exists. Skipping."))
                    continue  # Skip to next row
                
                product = Product.objects.create(
                    category=category,
                    name=row['title'],
                    slug=product_slug,
                    description=row.get('description', ''),
                    brand=row.get('brand', ''),
                    price=row.get('price', 0),
                    discount_percentage=row.get('discountPercentage', 0),
                    rating=row.get('rating', 0),
                    availability_status=row.get('availabilityStatus', ''),
                    stock=row.get('stock', 0),
                    tags=";".join(row.get('tags', '').split(';')),  
                    warranty_information=row.get('warrantyInformation', ''),
                    shipping_information=row.get('shippingInformation', ''),
                    return_policy=row.get('returnPolicy', ''),
                    sku=row.get('sku', ''),
                    weight=row.get('weight', 0),
                    dimensions=row.get('dimensions', ''),
                    thumbnail_url=row.get('thumbnail', ''),
                    is_featured=False,
                )

                if row.get('imageUrl'):
                    try:
                        response = requests.get(row['imageUrl'])
                        if response.status_code == 200:
                            img_name = f"{product_slug}.jpg"
                            product.image.save(img_name, ContentFile(response.content), save=True)
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"Image failed for '{row['title']}': {e}"))

        self.stdout.write(self.style.SUCCESS('Products loaded from CSV.'))
