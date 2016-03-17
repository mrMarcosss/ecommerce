from django.contrib import admin
from products.models import Product, Variation, ProductImage

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Variation)
