from django.shortcuts import render, redirect
from blog.forms import ShopComment, CommentForm
from shop.forms import Updateshop, ShopCreateForm, ProductCreateForm, Updateproduct, Wishlist, wishliststatus, postform
from .models import myshop, Product, wishlist, postinfo
from blog.models import SupCategory, Category, Comment, Comment_shop
from user_auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from shop.decorators import just_owner
import math
from PIL import Image
from persian_tools import digits

def all_views_navbar_utils(request):
    wish_op = digits.convert_to_fa(0)
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
        wish_op = digits.convert_to_fa(wish_op)
        same_context['wish'] = wish_op

        if request.user.owner:
            owner = True
            me = User.objects.get(mobile=request.user.mobile)
            my_shop = me.shop
            same_context['my_shop'] = my_shop
            same_context['owner'] = owner

    return same_context


def help(request):
    context = all_views_navbar_utils(request)
    return render(request, 'blog/help.html', context)


def all_products(request, slug):
    shop = myshop.objects.get(slug=slug)
    products = shop.products.all()
    context = {
        'shop': shop,
        'products': products,
    }
    context_same = all_views_navbar_utils(request)
    context.update(context_same)

    return render(request, 'shop/all_products.html', context)


def shop(request, slug):
    shop = myshop.objects.get(slug=slug)
    comments = Comment_shop.objects.filter(shop=shop).order_by('-date_posted')
    score = 0
    for i in range(0, len(comments)):
        score += int(comments[i].grade)
    if len(comments) != 0:
        final_score = score/len(comments)
    else:
        final_score = 0
    shop.grade = final_score
    final_score = math.ceil(final_score)
    shop.stars = final_score*'1'
    shop.stars_left = (5-final_score) * '1'
    shop.save()
    products_shop = shop.products.filter().order_by('-date')[0:8]
    rare = shop.products.filter(rare=True)[0:3]
    off = shop.products.filter(most_off=True)[0:3]
    hot = shop.products.filter(hot=True)[0:3]
    shop_m = [shop]
    if request.method == 'POST':
        form = ShopComment(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.feedbacker = request.user
            obj.save()
            obj.shop.set(shop_m)
            obj.save()
            obj.stars = obj.grade * '1'
            obj.save()
            obj.stars_left = (5 - obj.grade) * '1'
            obj.save()
            return redirect('shop',shop.slug)
    else:
        form = ShopComment()

    if request.user.is_anonymous:

        add_comment = False
    else:
        comments_me = comments.filter(feedbacker=request.user)
        j = 0
        for i in comments_me:
            j += 1

        if j > 3:
            add_comment = False
        else:
            add_comment = True
    comments = comments[0:10]
    context = {
        'products': products_shop,
        'add_comment': add_comment,
        'comments': comments,
        'shop': shop,
        'form': form,
        'rare': rare,
        'hot': hot,
        'off': off,
    }
    context_sample = all_views_navbar_utils(request)
    context.update(context_sample)
    return render(request, 'shop/shop.html', context)


@login_required(login_url='register')
@just_owner
def update_shop(request):
    me = User.objects.get(mobile=request.user.mobile)
    my_shop = me.shop
    shop = my_shop
    if request.method == 'POST':
        form = Updateshop(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('shop', shop.slug)
    else:
        form = Updateshop(instance=shop)
    context = {
            'my_shop': my_shop,
            'shop': shop,
            'form': form,
    }
    context_sample = all_views_navbar_utils(request)
    context.update(context_sample)
    return render(request, 'shop/update_shop.html', context)


@login_required(login_url='register')
def add_shop(request):
    if request.method == 'POST':
        form1 = ShopCreateForm(request.POST, request.FILES)
        user = request.user
        if form1.is_valid():
            obj = form1.save(commit=False)
            shop_slug = obj.slug
            obj.save()
            shop_o = myshop.objects.get(slug=shop_slug)
            user.shop = shop_o
            user.owner = True
            user.save()
            return redirect('home')
    else:
        form1 = ShopCreateForm()
        print(form1.errors)
    context = {
        'form': form1,
    }
    context_same = all_views_navbar_utils(request)
    context.update(context_same)
    return render(request, 'shop/add_shop.html', context)


@login_required(login_url='register')
@just_owner
def update_product(request, pk):
    me = User.objects.get(mobile=request.user.mobile)
    my_shop = me.shop
    shop = my_shop
    products = shop.products.all()
    product = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = Updateproduct(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('shop', shop.slug)
    else:
        form = Updateproduct(instance=product)

    context = {
            'shop': shop,
            'form': form,
            'products': products,
            'my_shop': my_shop,
    }
    context_sample = all_views_navbar_utils(request)
    context.update(context_sample)
    return render(request, 'shop/update_product.html', context)


@login_required(login_url='register')
@just_owner
def add_product(request):
    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            request.user.shop.products.add(obj)
            return redirect('shop', request.user.shop.slug)
    else:
        form = ProductCreateForm()
    context = {
        'form': form,
        'shop': request.user.shop,
    }
    context_sample = all_views_navbar_utils(request)
    context.update(context_sample)
    return render(request, 'shop/add_product.html', context)


def product_details(request, slug, pk):
    shop = myshop.objects.get(slug=slug)
    own = False
    product_details = shop.products.get(pk=pk)
    comments = Comment.objects.filter(products=product_details).order_by('-date_posted')
    score =0
    for i in range(0, len(comments)):
        score += int(comments[i].grade)
    if len(comments) != 0:
        final_score = score/len(comments)
    else:
        final_score = 0
    product_details.star_rate = final_score
    final_score = math.ceil(final_score)
    product_details.stars = final_score*'1'
    product_details.stars_left = (5-final_score) * '1'
    product_details.save()
    products = [product_details]
    if request.method == 'POST':
        if request.POST['action'] == 'comment':
            form1 = CommentForm(request.POST)
            form2 = Wishlist()
            if form1.is_valid():
                obj = form1.save(commit=False)
                obj.feedbacker = request.user
                obj.save()
                obj.products.set(products)
                obj.save()
                obj.stars = obj.grade*'1'
                obj.save()
                obj.stars_left = (5-obj.grade) * '1'
                obj.save()
                return redirect('product-details', slug,pk)
        elif request.POST['action'] == 'add_cart':
            form2 = Wishlist(request.POST)
            form1 = CommentForm()
            if form2.is_valid():
                obj = form2.save(commit=False)
                obj.shop = shop
                obj.buyer = request.user
                obj.product = product_details
                obj.save()
                return redirect('product-details', slug, pk)
        elif request.POST['action'] == 'change':
            form1 = CommentForm()
            form2 = Wishlist()
            return redirect('update_product', pk)
        elif request.POST['action'] == 'delete':
            my_shop = request.user.shop
            form1 = CommentForm()
            form2 = Wishlist()
            if my_shop.pk == shop.pk:
                my_shop.products.get(pk=pk).delete()
                return redirect('shop', slug)
    else:
        form1 = CommentForm()
        form2 = Wishlist()
    score_list = [None] * math.ceil(final_score)
    left_list = [None] * (5-math.ceil(final_score))
    final_score = math.ceil(final_score)
    ctg = Category.objects.get(name=product_details.category)
    related_products = Product.objects.filter(category=ctg)[0:4]

    if request.user.is_anonymous:

        add_comment = False
    else:
        comments_me = comments.filter(feedbacker=request.user)
        j=0
        for i in comments_me:
            j+=1

        if j>3:
            add_comment = False
        else:
            add_comment = True
    num_photos = 0
    if product_details.photo_3:
        num_photos += 1
    if product_details.photo_4:
        num_photos += 1
    if product_details.photo_5:
        num_photos += 1
    if product_details.photo_6:
        num_photos += 1
    any = True
    context = {
                'own': own,
                'any': any,
                'now': timezone.now,
                'num_photos': num_photos,
                'product': product_details,
                'related_products': related_products,
                'comments': comments,
                'form': form1,
                'form2': form2,
                'final_score': final_score,
                'score_list': score_list,
                'left_list': left_list,
                'shop': shop,
                'add_comment': add_comment,
    }
    context_sample = all_views_navbar_utils(request)
    context.update(context_sample)

    return render(request, 'shop/product-details.html', context)


@login_required(login_url='register')
def cart(request):
    if request.user.is_authenticated:
        if request.user.owner:
            owner = True
        else:
            owner = False
    wishlist_p = 0
    shop = myshop.objects.all()
    if request.method == "POST":
        pk = request.POST['action']
        wishlist_o = wishlist.objects.filter(pk=pk)
        wishlist_o.delete()
    if request.user.is_anonymous:
        is_owner = ""
        context = {
            'shop': shop,
            'is_owner': is_owner,
            'wish_list': wishlist_p,
        }
    else:
        wishlist_all = wishlist.objects.filter(buyer=request.user).filter(paid=False)
        all, off, op = 0, 0, 0
        for i in wishlist_all:
            wishlist_p += 1
            off += i.product.price * i.product.off/100
            op += i.product.price
  
        off = int(off)
        all_all = op-off
     
        context = {
            'off': f"{off:,}",
            'all_all': f"{all_all:,}",
            'all_price': f"{op:,}",
            'wish_list': wishlist_p,
            'wish_all': wishlist_all,
        }
    context_sample = all_views_navbar_utils(request)
    context.update(context_sample)
    return render(request, 'blog/cart.html', context)


@login_required(login_url='register')
def bought(request):
    wishlist_all = wishlist.objects.filter(buyer=request.user).filter(paid=True).order_by('-time_add')
    context = {
        'buy': wishlist_all,
    }
    context_sample = all_views_navbar_utils(request)
    context.update(context_sample)
    return render(request, 'blog/bought.html', context)
    
    
@login_required(login_url='register')
@just_owner
def sold(request):
    my_shop = request.user.shop
    wish_sold = wishlist.objects.filter(shop=my_shop).filter(paid=True).order_by('-time_add')
    context = {
        'sold': wish_sold,
    }
    context_sample = all_views_navbar_utils(request)
    context.update(context_sample)
    return render(request, 'blog/sold.html', context)


@login_required(login_url='register')
@just_owner
def sold_detail(request, pk):
    my_shop = request.user.shop
    wish_sold = wishlist.objects.filter(shop=my_shop)
    wish_sold = wish_sold.get(pk=pk)
    if request.method == 'POST':
        form = wishliststatus(request.POST, instance=wish_sold)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            return redirect('sold-detail', pk)
    else:
        form = wishliststatus(instance=wish_sold)
    context = {
        'sold': wish_sold,
        'form': form,
    }
    context_sample = all_views_navbar_utils(request)
    context.update(context_sample)
    return render(request, 'blog/sold_detail.html', context)
    
    
@login_required(login_url='register')
def post_info(request):
    wish_me = wishlist.objects.filter(buyer=request.user).filter(paid=False)
    post_m = postinfo.objects.filter(user=request.user).order_by('-time_add').first()
    if request.method == 'POST':
        form = postform(request.POST, instance=post_m)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            for x in wish_me:
                x.post_info = obj
                x.save()
            return redirect('go-to-shop')
    else:
        form = postform(instance=post_m)
    context = {
        'form': form,
    }
    context_sample = all_views_navbar_utils(request)
    context.update(context_sample)
    return render(request, 'blog/post_info.html', context)


def page_404(request, exception):
    return render(request, '404.html', status=404)


def page_403(request, exception):
    return render(request, '403.html', status=403)


def page_500(request, exception):
    return render(request, '500.html', status=500)


def page_400(request, exception):
    return render(request, '400.html', status=400)