from django.core.management.base import BaseCommand
from store.models import Category, Product
from django.utils.text import slugify

class Command(BaseCommand):
    help = "Seed database with sample categories and products"

    def handle(self, *args, **options):
        categories = ['Electronics', 'Books', 'Clothing', 'Accessories']
        category_objs = []

        for cat in categories:
            slug = slugify(cat)
            obj, created = Category.objects.get_or_create(name=cat, slug=slug)
            category_objs.append(obj)

        products = [
            {'name': 'Smartphone', 'price': 15000, 'category': category_objs[0]},
            {'name': 'Laptop', 'price': 55000, 'category': category_objs[0]},
            {'name': 'Python Book', 'price': 500, 'category': category_objs[1]},
            {'name': 'T-Shirt', 'price': 700, 'category': category_objs[2]},
            {'name': 'Wrist Watch', 'price': 1200, 'category': category_objs[3]},
        ]

        for p in products:
            Product.objects.get_or_create(name=p['name'], price=p['price'], category=p['category'])

        self.stdout.write(self.style.SUCCESS('Sample categories and products added successfully!'))
