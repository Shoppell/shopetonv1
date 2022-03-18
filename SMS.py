from os import link
from random import randint
from melipayamak import Api
from django.utils.timezone import timedelta
from django.utils import timezone
from .models import User

username = '09930731973'
password = 'D9HTC'
api = Api(username, password)

def  product_registered_customer(mobile, link1):      
    sms_rest = api.sms()
    text = [link1 ]
    to = mobile
    bodyId = 79817
    sms_rest.send_by_base_number(text, to, bodyId)

def  product_registered_seller (mobile, link1):  
    sms_rest = api.sms()
    text = [link1 ]
    to = mobile
    bodyId = 79832
    sms_rest.send_by_base_number(text, to, bodyId)


def  Store_registered (mobile, linkedit,linkproduct):  
    sms_rest = api.sms()
    text =linkedit+';'+linkproduct
    to = mobile
    bodyId = 79820
    sms_rest.send_by_base_number(text, to, bodyId)

def  Add_store_card_number (mobile, linkedit):  
    sms_rest = api.sms()
    text = [linkedit ]
    to = mobile
    bodyId = 79821
    sms_rest.send_by_base_number(text, to, bodyId)

def  status_changing  (mobile, text1):  
    sms_rest = api.sms()
    text = [text1 ]
    to = mobile
    bodyId = 79830
    sms_rest.send_by_base_number(text, to, bodyId)

def  money_deposited  (mobile, link1):  
    sms_rest = api.sms()
    text = [link1 ]
    to = mobile
    bodyId = 79833
    sms_rest.send_by_base_number(text, to, bodyId)

def  message_from_seller(mobile,text1,link1):  
    sms_rest = api.sms()
    text =text1+';'+link1
    to = mobile
    bodyId = 80085
    sms_rest.send_by_base_number(text, to, bodyId)

def  message_from_customer(mobile,text1,link1):  
    sms_rest = api.sms()
    text =text1+';'+link1
    to = mobile
    bodyId = 80084
    sms_rest.send_by_base_number(text, to, bodyId)


def  commodity_registration_error(mobile,link1):  
    sms_rest = api.sms()
    text = [link1 ]
    to = mobile
    bodyId = 80086
    sms_rest.send_by_base_number(text, to, bodyId)