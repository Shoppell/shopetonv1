from django import forms
from user_auth.models import User
from blog.models import contact_with_us, Comment_shop, ticket, Comment

        
class Contact(forms.ModelForm):
    class Meta:
        model = contact_with_us
        fields = ['content', 'name']


class ChangeProfile(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class RegisterTicket(forms.ModelForm):

    class Meta:
        model = ticket
        exclude = ['user', 'is_answerd', 'date_posted', 'answer']


class ShopComment(forms.ModelForm):

    class Meta:
        model = Comment_shop
        fields = ('grade', 'content')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.Textarea)

    class Meta:
        model = User
        fields = ['mobile', 'email']


class UserRegisterationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['mobile']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('grade','content')

