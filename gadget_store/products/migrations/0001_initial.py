# Generated by Django 5.1.7 on 2025-05-14 23:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('image', models.ImageField(upload_to='products/')),
                ('description', models.TextField()),
                ('brand', models.CharField(blank=True, max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount_percentage', models.FloatField(default=0.0)),
                ('rating', models.FloatField(default=0.0)),
                ('rating_count', models.PositiveIntegerField(default=0)),
                ('availability_status', models.CharField(blank=True, max_length=100)),
                ('stock', models.PositiveIntegerField(default=1)),
                ('tags', models.CharField(blank=True, max_length=300)),
                ('warranty_information', models.TextField(blank=True)),
                ('shipping_information', models.TextField(blank=True)),
                ('return_policy', models.TextField(blank=True)),
                ('sku', models.CharField(blank=True, max_length=100)),
                ('weight', models.FloatField(default=0.0)),
                ('dimensions', models.CharField(blank=True, max_length=100)),
                ('thumbnail_url', models.URLField(blank=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'product')},
            },
        ),
    ]
