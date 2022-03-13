
from django.db import models
from django.contrib.auth.models import AbstractUser
from user_auth.myusermanager import MyUserManager
from shop.models import myshop


class User(AbstractUser):
    username = None
    mobile = models.CharField(max_length=11, unique=True)
    otp = models.PositiveIntegerField(blank=True, null=True)
    otp_create_time = models.DateTimeField(auto_now=True)
    shop = models.OneToOneField(myshop, blank=True, on_delete=models.CASCADE, null=True)
    owner = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = []

    backend = 'user_auth.mybackend.MobileBackend'

    def hide_mobile(self):
        mobile = self.mobile[6:11]
        hidden_mobile =  '******' + mobile
        return hidden_mobile
