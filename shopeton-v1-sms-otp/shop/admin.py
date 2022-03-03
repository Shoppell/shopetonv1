from django.contrib import admin
from .models import myshop, Product, wishlist, Order, postinfo

admin.site.register(postinfo)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(wishlist)
admin.site.register(myshop)
