from django.urls import path
from . import views
from shop.views import add_shop,  cart, add_product, update_shop, update_product, post_info, bought, sold, sold_detail
from blog.views import one_product

urlpatterns = [
    path('shop/<slug:slug>/', views.shop, name='shop'),
    path('shop/<slug:slug>/product/<int:pk>', views.product_details, name='product-details'),
    path('shop/<slug:slug>/all_products/', views.all_products, name='all_products'),
    path('update_product/<int:pk>', update_product, name='update_product'),
    path('update_shop/', update_shop, name='update_shop'),
    path('one_product/<int:pk>', one_product, name='one_product'),
    path('cart/', cart, name='cart'),
    path('bought/', bought, name='bought'),
    path('sold/', sold, name='sold'),
    path('sold/<int:pk>', sold_detail, name='sold-detail'),
    path('post_info/', post_info, name='post-info'),
    path('addproduct/', add_product, name='add_product'),
    path('addshop/', add_shop, name='add_shop'),
]
