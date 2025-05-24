import csv
import os
from django.core.management.base import BaseCommand
from products.models import Product, Category
from django.utils.text import slugify
from django.conf import settings
from django.core.files.base import ContentFile
import requests

MAX_CATEGORY_NAME_LENGTH = 500
MAX_CATEGORY_SLUG_LENGTH = 500
MAX_PRODUCT_SLUG_LENGTH = 500

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
                # Truncate category name and slug to max length to avoid DB errors
                raw_category_name = row.get('category', 'Uncategorized').strip()
                category_name = raw_category_name[:MAX_CATEGORY_NAME_LENGTH]
                category_slug = slugify(category_name)[:MAX_CATEGORY_SLUG_LENGTH]

                category, created = Category.objects.get_or_create(
                    slug=category_slug,
                    defaults={'name': category_name}
                )
                if not created and category.name != category_name:
                    # If slug existed but name differs, optionally update name or skip
                    category.name = category_name
                    category.save()

                # Slugify product title and limit length
                raw_title = row.get('title', '').strip()
                if not raw_title:
                    self.stdout.write(self.style.WARNING("Skipping product with empty title."))
                    continue
                product_slug = slugify(raw_title)[:MAX_PRODUCT_SLUG_LENGTH]

                # Check if product exists already
                if Product.objects.filter(slug=product_slug).exists():
                    self.stdout.write(self.style.WARNING(f"Product '{raw_title}' already exists. Skipping."))
                    continue

                # Helper to safely parse float/int or default
                def safe_float(val, default=0.0):
                    try:
                        return float(val)
                    except (TypeError, ValueError):
                        return default

                def safe_int(val, default=0):
                    try:
                        return int(float(val))  # In case val is "10.0"
                    except (TypeError, ValueError):
                        return default

                product = Product.objects.create(
                    category=category,
                    name=raw_title,
                    slug=product_slug,
                    description=row.get('description', '').strip(),
                    brand=row.get('brand', '').strip(),
                    price=safe_float(row.get('price', 0)),
                    discount_percentage=safe_float(row.get('discountPercentage', 0)),
                    rating=safe_float(row.get('rating', 0)),
                    rating_count=safe_int(row.get('ratingCount', 0)),
                    availability_status=row.get('availabilityStatus', '').strip(),
                    stock=safe_int(row.get('stock', 1)),
                    tags=";".join([t.strip() for t in row.get('tags', '').split(';') if t.strip()]),
                    warranty_information=row.get('warrantyInformation', '').strip(),
                    shipping_information=row.get('shippingInformation', '').strip(),
                    return_policy=row.get('returnPolicy', '').strip(),
                    sku=row.get('sku', '').strip(),
                    weight=safe_float(row.get('weight', 0)),
                    dimensions=row.get('dimensions', '').strip(),
                    thumbnail_url=row.get('thumbnail', '').strip(),
                    is_featured=False,
                )

                image_url = row.get('imageUrl', '').strip()
                if image_url:
                    try:
                        response = requests.get(image_url)
                        if response.status_code == 200:
                            img_name = f"{product_slug}.jpg"
                            product.image.save(img_name, ContentFile(response.content), save=True)
                        else:
                            self.stdout.write(self.style.WARNING(f"Image download failed for '{raw_title}': HTTP {response.status_code}"))
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"Image failed for '{raw_title}': {e}"))

        self.stdout.write(self.style.SUCCESS('Products loaded from CSV.'))
