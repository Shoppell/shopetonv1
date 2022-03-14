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
        exclude = ['head_link', 'about', 'image_look', 'title_look', 'description_look', 'products', 'owner', 'h_index', 'grade', 'stars', 'stars_left', 'why_us1', 'why_us2', 'why_us3', 'image_banner1', 'image_banner2', 'image_banner3']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'فروشگاه لباس علی'}),
            'slug': forms.TextInput(attrs={'placeholder': 'foroshgahali'}),
            'phone': forms.TextInput(attrs={'placeholder': '0283378****'}),
            'head_title': forms.TextInput(attrs={'placeholder': 'لباس علی'}),
            'head_description': forms.TextInput(attrs={'placeholder': 'بهترین کیفیت و شرایط'}),
            'address': forms.TextInput(attrs={'placeholder': 'تهران تهران خیابان حافظ'}),
            'seller_info': forms.TextInput(attrs={'placeholder': 'با شماره ی فروشگاه تماس حاصل شود'}),
            'bank_account': forms.TextInput(attrs={'placeholder': '6037701689095443'}),
        }


class UserShop(forms.ModelForm):

    class Meta:
        model = User
        fields = ['shop', 'mobile']


class UpdateWishlist(forms.ModelForm):

    class Meta:
        model = wishlist
        exclude = ['buyer', 'product', 'paid', 'time_add', ' post_info', 'status']


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
