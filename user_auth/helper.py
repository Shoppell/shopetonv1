from random import randint
from .models import User
from django.utils.timezone import timedelta
from django.utils import timezone
from melipayamak import Api

username = '09930731973'
password = 'D9HTC'

def send_otp(mobile, otp): 
    api = Api(username, password)
    sms_rest = api.sms()
    text = [otp, ]
    to = mobile
    bodyId = 77985
    sms_rest.send_by_base_number(text, to, bodyId)


def otp_generator():
    return randint(1000, 9999)


def check_otp_expiration(mobile):
    try:
        user = User.objects.get(mobile=mobile)
        now = timezone.now()
        otp_time = user.otp_create_time
        otp_after = otp_time + timedelta(seconds=180)
        if now > otp_after:
            return False
        return True

    except User.DoesNotExist:
        return False
