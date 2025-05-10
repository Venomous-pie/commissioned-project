import csv
import random
import os
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify
from products.models import Product, Category
from django.conf import settings
from faker import Faker
import requests

fake = Faker()

# Tech image URLs as placeholders (can be expanded as needed)
TECH_IMAGE_URLS = [
    "https://images.unsplash.com/photo-1517336714731-489689fd1ca8",  # Laptop
    "https://images.unsplash.com/photo-1510552776732-43f6d005dd22",  # Smartphone
    "https://images.unsplash.com/photo-1587829741301-dc798b83add3",  # Smartwatch
    "https://images.unsplash.com/photo-1549924231-f129b911e442",     # Drone
    "https://images.unsplash.com/photo-1580894894513-379c7f55f080",  # Monitor
    "https://images.unsplash.com/photo-1549924231-88c3c45f90c3",     # Console
    "https://images.unsplash.com/photo-1603791440384-56cd371ee9a7",  # Tablet
]

class Command(BaseCommand):
    help = 'Import products from CSV, creating categories and generating products'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file containing category paths')
        parser.add_argument('--limit', type=int, default=100, help='Limit the number of products to import')
        parser.add_argument('--reset', action='store_true', help='Reset the database before importing (delete existing products and categories)')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        limit = options['limit']
        reset = options['reset']
        
        if not os.path.exists(csv_file):
            self.stderr.write(self.style.ERROR(f"File {csv_file} does not exist!"))
            return

        # Reset the database if requested
        if reset:
            self.stdout.write(self.style.WARNING("Resetting database (deleting existing products and categories)..."))
            Product.objects.all().delete()
            Category.objects.all().delete()

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            categories_created = 0
            products_created = 0
            category_objs = {}

            for row in reader:
                if len(row) < 6:
                    continue  # Skip invalid rows
                
                # Parse category path
                category_path = [category.strip() for category in row]
                parent_category = None

                # Create categories based on the category path
                for category_name in category_path:
                    if category_name:  # Skip empty strings
                        category_slug = slugify(category_name)
                        if category_slug not in category_objs:
                            category_objs[category_slug], created = Category.objects.get_or_create(
                                name=category_name, slug=category_slug, parent=parent_category if parent_category else None
                            )
                            if created:
                                categories_created += 1
                        parent_category = category_objs[category_slug]

                # Generate a fake product for each category path
                for _ in range(3):  # Generate 3 products per category for variety
                    if products_created >= limit:
                        self.stdout.write(self.style.SUCCESS(f"Reached the product limit: {limit}"))
                        break

                    product_name = fake.word().capitalize() + " " + fake.word().capitalize()
                    product_slug = slugify(product_name)
                    description = fake.paragraph(nb_sentences=3)
                    price = round(random.uniform(20, 1000), 2)
                    image_url = random.choice(TECH_IMAGE_URLS)

                    # Check if the product already exists
                    if Product.objects.filter(slug=product_slug).exists():
                        continue

                    # Create the product
                    product = Product(
                        name=product_name,
                        slug=product_slug,
                        description=description,
                        price=price,
                        category=parent_category,
                        stock=10,  # Default stock
                        is_featured=False,
                    )

                    # Download the image if URL is available
                    image_content = self.download_image(image_url)
                    if image_content:
                        image_name = f"{product_slug}.jpg"
                        product.image.save(image_name, ContentFile(image_content), save=True)

                    # Save the product
                    product.save()
                    products_created += 1

            self.stdout.write(self.style.SUCCESS(f"{categories_created} categories and {products_created} products created."))

    def download_image(self, image_url):
        try:
            response = requests.get(image_url, timeout=5)
            if response.status_code == 200:
                return response.content
        except Exception:
            self.stderr.write(self.style.ERROR(f"Failed to download image from: {image_url}"))
        return None
