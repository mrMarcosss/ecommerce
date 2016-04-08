from django.contrib import admin
from products.models import Product, Variation, ProductImage, Category

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Variation)
