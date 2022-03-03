from django.shortcuts import render
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import forms
from .models import User
from . import helper
from django.utils.timezone import timedelta
from django.utils import timezone


def verify(request):
    try:
        mobile = request.session.get('user_mobile')
        user = User.objects.get(mobile=mobile)
        if request.method == "POST":
            if not helper.check_otp_expiration(user.mobile):
                return HttpResponseRedirect(reverse('register_view'))

            if user.otp != int(request.POST.get('otp')):
                return HttpResponseRedirect(reverse('register_view'))
            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('home'))

        return render(request, 'blog/verify.html', {'mobile': mobile})
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('register_view'))


def register_view(request):
    form = forms.RegisterForm

    if request.method == "POST":
        try:
            if "mobile" in request.POST:
                mobile = request.POST.get('mobile')
                user = User.objects.get(mobile=mobile)
                last_time = user.otp_create_time+timedelta(seconds=30)
                if timezone.now() > last_time:
                    otp = helper.otp_generator()
                    helper.send_otp(mobile, otp)
                    user.otp = otp
                user.save()
                request.session['user_mobile'] = user.mobile
                return HttpResponseRedirect(reverse('verify'))

        except User.DoesNotExist:
            form = forms.RegisterForm(request.POST)

            if form.is_valid():
                mobile = request.POST.get('mobile')
                user = form.save(commit=False)
                otp = helper.otp_generator()
                helper.send_otp(mobile, otp)
                user.otp = otp
                user.is_active = False
                user.save()
                request.session['user_mobile'] = user.mobile
                return HttpResponseRedirect(reverse('verify'))
    return render(request, 'blog/register.html', {'form': form})


def dashboard(request):
    return render(request, 'dashboard.html')
