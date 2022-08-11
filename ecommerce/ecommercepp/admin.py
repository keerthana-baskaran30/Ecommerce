""" used to display models in the Django admin panel."""
from django.contrib import admin
from ecommercepp.models import Customer, Product, Cart, Seller


admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Seller)
admin.site.register(Customer)
