from django.shortcuts import render, redirect
from .forms import Contact, ChangeProfile, RegisterTicket
from shop.models import myshop, Product, wishlist
from blog.models import ticket, SupCategory, Category
from user_auth.models import User
from django.contrib.auth.decorators import login_required
import logging
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import HttpResponse, Http404
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from shop.decorators import just_owner

@login_required
def callback_gateway_shop(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        # پرداخت با موفقیت انجام پذیرفته است و بانک تایید کرده است.
        # می توانید کاربر را به صفحه نتیجه هدایت کنید یا نتیجه را نمایش دهید.
        cart = wishlist.objects.filter(buyer=request.user).filter(paid=False).update(paid=True)

     
        return redirect('bought')

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    return HttpResponse("پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.")


@login_required
def go_to_gateway_shop(request):
    
    my_cart = wishlist.objects.filter(paid=False).filter(buyer=request.user)
    amount = 0
    for x in my_cart:
        amount += x.product.last_price()
        
    amount = amount*10
    user_mobile_number = '+989112221234'  # اختیاری
        
    factory = bankfactories.BankFactory()
    try:
        bank = factory.auto_create() # or factory.create(bank_models.BankType.BMI) or set identifier
        bank.set_request(request)
        bank.set_amount(amount)
        # یو آر ال بازگشت به نرم افزار برای ادامه فرآیند
        bank.set_client_callback_url(reverse('callback-shop'))
        bank.set_mobile_number(user_mobile_number)  # اختیاری
    
        # در صورت تمایل اتصال این رکورد به رکورد فاکتور یا هر چیزی که بعدا بتوانید ارتباط بین محصول یا خدمات را با این
        # پرداخت برقرار کنید. 
        bank_record = bank.ready()
        
        # هدایت کاربر به درگاه بانک
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        # TODO: redirect to failed page.
        raise e


def all_views_navbar_utils(request):
    wish_op = 0
    login = False

    same_context = {
        'wish': wish_op,
        'login': login,
        'scategory': SupCategory.objects.all(),
    }

    if request.user.is_authenticated:
        login = True
        if wishlist.objects.filter(buyer=request.user).filter(paid=False).exists():
            wish_op = wishlist.objects.filter(buyer=request.user).filter(paid=False).__len__()
        else:
            wish_op = 0
        same_context['login'] = login
        same_context['wish'] = wish_op

        if request.user.owner:
            owner = True
            me = User.objects.get(mobile=request.user.mobile)
            my_shop = me.shop
            same_context['my_shop'] = my_shop
            same_context['owner'] = owner

    return same_context


def supcategory(request, pk):
    sup = SupCategory.objects.get(pk=pk)
    context_same = {
          'sup':sup,
    }
    context = all_views_navbar_utils(request)
    context.update(context_same)

    return render(request, 'blog/supcategory.html', context)


def category(request, pk):

    part = 4
    category_p = Category.objects.get(pk=pk)
    all = Product.objects.filter(category=category_p).__len__()
    if request.method=='POST':
        if request.POST['num']:
            num = request.POST['num']
            if int(num)==all:
                part = int(num)
            else:
                part = int(num) + 4
    products =Product.objects.filter(category=category_p)[0:part]
    context = {

        'products': products,
        'num_product': part,
        'category': category_p,
    }
    context_sample = all_views_navbar_utils(request)
    context.update(context_sample)

    return render(request, 'blog/category.html', context)


def about_us(request):
    context = all_views_navbar_utils(request)
    return render(request, 'blog/about_us.html', context)


def search(request):
    search = ''
    context = {
        'all_product': Product.objects.filter(name__contains=search),
        'all_shop': myshop.objects.filter(title__contains=search),
    }
    if request.method == 'POST':
        search = request.POST['action']
        context_sample = {
            'searched': search,
        }
        context.update(context_sample)
    context_get = all_views_navbar_utils(request)
    context.update(context_get)

    return render(request, 'blog/search.html', context)


def contact(request):

    if request.method == 'POST':
        form = Contact(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('contact')
    else:
        form = Contact()

    context = all_views_navbar_utils(request)
    context['form'] = form

    return render(request, 'blog/contact_us.html', context)


@login_required
def profile(request):

    user = request.user

    if request.method == 'POST':
        form = ChangeProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
    else:
        form = ChangeProfile(instance=user)

    context = all_views_navbar_utils(request)
    context['form'] = form

    return render(request, 'blog/profile.html', context)


@login_required
@just_owner
def my_tickets(request):

    if request.method == 'POST':
        form = RegisterTicket(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('my_ticket')
    else:
        form = RegisterTicket()

    tickets = ticket.objects.filter(user=request.user).order_by('-date_posted')[0:10]

    context = all_views_navbar_utils(request)
    context['form'] = form
    context['tickets'] = tickets

    return render(request, 'blog/my_tickets.html', context)


def one_product(request, pk):
    product = Product.objects.get(pk=pk)
    shop = myshop.objects.get(products=product)

    return redirect('product-details', shop.slug, pk)


def home(request):
    k = 8
    rate = False
    verify = False
    exists = False
    rate_product = False
    all_products = Product.objects.all()[0:k]
    all_shop = myshop.objects.all()[0:k]
    category_m = Category.objects.all()

    if request.method == 'POST':
        value = request.POST['action']
        if value == 'rate':
            rate = True
        if value == 'verify':
            verify = True
        if value == 'rate-product':
            rate_product = True
        if value == 'exists':
            exists = True
    if rate:
        all_shop = myshop.objects.order_by('-grade')[:k]

    if verify:
        all_shop = myshop.objects.filter(verified=True)

    if exists:
        all_products = Product.objects.filter(in_stock=True)

    if rate_product:
        all_products = Product.objects.order_by('-star_rate')[:k]

    context_same = all_views_navbar_utils(request)

    context = {
                'all_product': all_products,
                'all_shop': all_shop,
                'rate': rate,
                'verify': verify,
                'rate_p': rate_product,
                'exists': exists,
                'form': 'form',
                'category': category_m,
                'hot': Product.objects.filter(hot=True)[0:8],
                'off': Product.objects.filter(most_off=True)[0:8],
                'rare': Product.objects.filter(rare=True)[0:8],
    }

    context.update(context_same)

    return render(request, 'blog/home.html', context)


def page_404(request, exception):
    return render(request, '404.html', status=404)


def page_403(request, exception):
    return render(request, '403.html', status=403)


def page_500(request, exception):
    return render(request, '500.html', status=500)


def page_400(request, exception):
    return render(request, '400.html', status=400)
