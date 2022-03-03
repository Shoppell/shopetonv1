import requests
from random import randint
from .models import User
import datetime
from django.utils.timezone import timedelta
from django.utils import timezone


def send_otp(mobile, otp):
    url = 'https://rest.payamak-panel.com/api/SendSMS/SendSMS'
    myobj = {'username': '09930731973',
             'password': 'D9HTC',
             'to': mobile,
             'from': '50004001731973',
             'text': otp
             }

    x = requests.post(url, data=myobj)
    print(x.text)


def otp_generator():
    return randint(1000, 9999)


def check_otp_expiration(mobile):
    try:
        user = User.objects.get(mobile=mobile)
        now = timezone.now()
        otp_time = user.otp_create_time
        otp_after = otp_time + timedelta(seconds=30)
        if now > otp_after:
            return False
        return True

    except User.DoesNotExist:
        return False
