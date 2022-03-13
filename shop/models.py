from django.db import models
from django.utils import timezone


choices_post = (
    ('کالا در حال آماده سازی برای ارسال است', 'کالا در حال آماده سازی برای ارسال است'),
    ('کالا تحویل پست داده شد', 'کالا تحویل پست داده شد'),
)


choices_rate = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)
from PIL import Image
from persian_tools import digits, separator

def resize(nameOfFile):
    img = Image.open(nameOfFile)
    size = (200, int(img.size[1] * 200 / img.size[0]))
    img.resize(size, Image.ANTIALIAS).save(nameOfFile)
    img.save(nameOfFile)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام کالا')
    photo = models.ImageField(upload_to='products', verbose_name='عکس اول کالا')
    photo_2 = models.ImageField(upload_to='products', blank=True, verbose_name='عکس دوم کالا')
    photo_3 = models.ImageField(upload_to='products', blank=True, verbose_name='عکس سوم کالا')
    photo_4 = models.ImageField(upload_to='products', blank=True, verbose_name='عکس چهارم کالا')
    photo_5 = models.ImageField(upload_to='products', blank=True, verbose_name='عکس پنجم کالا')
    photo_6 = models.ImageField(upload_to='products', blank=True, verbose_name='عکس ششم کالا')
    price = models.IntegerField(verbose_name='قیمت کالا| بدون تخفیف')
    off = models.PositiveIntegerField(verbose_name='تخفیف')
    details = models.TextField(verbose_name='درباره ی کالا')
    category = models.ForeignKey(to='blog.Category', on_delete=models.CASCADE, verbose_name='دسته ی کالا')
    date = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت کالا')
    hot = models.BooleanField(default=False, verbose_name='کالا داغ است؟')
    most_off = models.BooleanField(default=False, verbose_name='کالا پر تخفیف است؟')
    rare = models.BooleanField(default=False, verbose_name='کالا بسیار ویژه است؟')
    in_stock = models.BooleanField(default=True, verbose_name='کالا موجود است؟')
    star_rate = models.PositiveIntegerField(blank=True, default=0)
    stars = models.CharField(default=0, max_length=5)
    stars_left = models.CharField(blank=True, max_length=5)

    def save(self, *args, **kwargs):
        for x in [self.photo, self.photo_2, self.photo_3, self.photo_4, self.photo_5, self.photo_6]:
            if x:
                super().save(*args, **kwargs)
                resize(x.path)

    def last_price(self):
        english_number = (100-self.off)*self.price/100
        persian_number = round(float(digits.convert_to_fa(english_number)))
        return persian_number
        
    def price_comma(self):
        persian_number = digits.convert_to_fa(self.price)
        persian_number = separator.add(persian_number)  
        return persian_number
    
    def last_comma(self):
        lprice = int((100-self.off)*self.price/100)
        persian_number = digits.convert_to_fa(lprice) 
        persian_number = separator.add(persian_number) 
        return persian_number

    def persian_off(self):
        off = self.off
        off = digits.convert_to_fa(off)
        return off

    def __str__(self):
        return self.name


class myshop(models.Model):
    products = models.ManyToManyField(Product, blank=True, verbose_name='محصولات')
    title = models.CharField(max_length=30,verbose_name='اسم فروشگاه')
    head_title = models.CharField(max_length=100,verbose_name='عنوان سر تیتر')
    head_description = models.CharField(max_length=80, verbose_name='توضیحات سر تیتر')
    head_link = models.TextField(blank=True, verbose_name='لینک تیتر')
    image_head1 = models.ImageField(upload_to="shops.head", verbose_name='عکس تیتر اول')
    slug = models.SlugField(unique=True, verbose_name='آیدی فروشگاه شما')
    phone = models.CharField(max_length=30, verbose_name='تلفن شما')
    phone_bool = models.BooleanField(default=False, verbose_name='تلفن شما نمایش داده شود؟')
    address = models.TextField(verbose_name='آدرس شما')
    address_bool = models.BooleanField(default=False, verbose_name='آدرس شما نمایش داده شود؟')
    why_us1 = models.CharField(blank=True, max_length=50, verbose_name='عنوان اول چرا ما')
    why_us2 = models.CharField(blank=True, max_length=50, verbose_name='عنوان دوم چرا ما')
    why_us3 = models.CharField(blank=True, max_length=50, verbose_name='عنوان سوم چرا ما')
    image_banner1 = models.ImageField(blank=True, upload_to="shops.banner", verbose_name='عکس بنر اول')
    image_banner2 = models.ImageField(blank=True, upload_to="shops.banner", verbose_name='عکس بنر دوم')
    image_banner3 = models.ImageField(blank=True, upload_to="shops.banner", verbose_name='عکس بنر سوم')
    image_look = models.ImageField(blank=True, upload_to="shops.look", verbose_name='عکس پوستر')
    title_look = models.CharField(blank=True, max_length=50, verbose_name='عنوان پوستر')
    description_look = models.TextField(blank=True, verbose_name='توضیحات پوستر')
    h_index = models.IntegerField(default=0, verbose_name='رتبه ی فروشگاه')
    grade = models.PositiveIntegerField(default=0, verbose_name='رتبه بر اساس نظرات')
    stars = models.CharField(default=0, max_length=5)
    stars_left = models.CharField(blank=True, max_length=5)
    verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    time_created = models.DateTimeField(default=timezone.now, blank=True, verbose_name='زمان ساخت فروشگاه')
    seller_info = models.CharField(max_length=150)
    about = models.TextField(blank=True, verbose_name='درباره ی فروشگاه')

    def save(self, *args, **kwargs):
        for x in [self.image_head1, self.image_banner1, self.image_banner2, self.image_banner3, self.image_look]:
            if x:
                super().save(*args, **kwargs)
                resize(x.path)

    def __str__(self):
        return self.title


class postinfo(models.Model):
    user = models.ForeignKey(to='user_auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    family_name = models.CharField(max_length=200)
    address = models.TextField()
    postal_code = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    time_add = models.DateTimeField(default=timezone.now,verbose_name='زمان اضافه شدن')


class wishlist(models.Model):
    post_info = models.ForeignKey(postinfo,blank=True,null=True, on_delete=models.CASCADE,verbose_name='اطلاعات ارسال')
    shop = models.ForeignKey(myshop, on_delete=models.CASCADE,verbose_name='نام فروشگاه')
    buyer = models.ForeignKey(to='user_auth.User', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='نام محصول')
    paid = models.BooleanField(default=False,verbose_name='پرداخت شده؟')
    time_add = models.DateTimeField(default=timezone.now,verbose_name='زمان اضافه شدن')
    status = models.CharField(max_length=100,blank=True,null=True,choices=choices_post, verbose_name='وضعیت ارسال کالا')

    def __str__(self):
        return self.buyer.mobile+str(self.shop)
