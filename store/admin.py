from django.contrib import admin
from .models import Category, Product, Order, OrderItem

# admin.site.register(Category)
# admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
from django.contrib import admin
from .models import Product, Category
from django.utils.html import format_html

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'image_tag', 'image_url')

    # Optional: show image preview in admin
    def image_tag(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" style="height:50px;" />', obj.image_url)
        return "-"
    image_tag.short_description = 'Image'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
