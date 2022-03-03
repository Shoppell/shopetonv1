from django import forms
from shop.models import myshop, wishlist, Product, postinfo
from user_auth.models import User


class wishliststatus(forms.ModelForm):
    class Meta:
        model = wishlist
        fields = ['status']


class postform(forms.ModelForm):
    class Meta:
        model = postinfo
        exclude = ['user', 'time_add']


class Updateshop(forms.ModelForm):
    class Meta:
        model = myshop
        exclude = ['products', 'h_index', 'owner', 'slug', 'grade', 'stars']


class ShopCreateForm(forms.ModelForm):

    class Meta:
        model = myshop
        exclude = ['products', 'owner', 'h_index', 'grade', 'stars', 'stars_left']


class UserShop(forms.ModelForm):

    class Meta:
        model = User
        fields = ['shop', 'mobile']


class UpdateWishlist(forms.ModelForm):

    class Meta:
        model = wishlist
        exclude = ['buyer', 'product', 'paid', 'time_add',' post_info','status']


class Wishlist(forms.ModelForm):

    class Meta:
        model = wishlist
        exclude = ['buyer', 'product', 'paid', 'time_add', 'shop', 'post_info', 'status']


class Updateproduct(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['user', 'count_out_stock', 'stars']


class ProductCreateForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ['user', 'inventory', 'count_out_stock', 'stars', 'stars_left', 'star_rate']
