from django.db import models
from extensions.utils import jalali_converter
from django.utils import timezone
from shop.models import Product, myshop

choices_rate = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)
from PIL import Image


def resize(nameOfFile):
    img = Image.open(nameOfFile)
    size = (200, int(img.size[1] * 200 / img.size[0]))
    img.resize(size, Image.ANTIALIAS).save(nameOfFile + '_resized' + nameOfFile[-4:])
    img.save(nameOfFile)


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name="اسم دسته")
    photo = models.ImageField(upload_to='products_category', verbose_name='عکس دسته')
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        for x in [self.photo, ]:
            if x:
                super().save(*args, **kwargs)
                resize(x.path)

    def __str__(self):
        return self.name


class SupCategory(models.Model):
    name = models.CharField(max_length=30, verbose_name="اسم دسته")
    photo = models.ImageField(upload_to='products_category', verbose_name='عکس سر دسته')
    categories = models.ManyToManyField(Category)
    date = models.DateTimeField(auto_now_add=True)
    svg = models.TextField()

    def save(self, *args, **kwargs):
        for x in [self.photo, ]:
            if x:
                super().save(*args, **kwargs)
                resize(x.path)

    def __str__(self):
        return self.name


class Comment(models.Model):
    feedbacker = models.ForeignKey(to='user_auth.User', on_delete=models.CASCADE, blank=True, null=True,verbose_name='ارسال کننده ی نظر')
    content = models.TextField(verbose_name='محتوای کامنت')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='زمان ارسال کامنت')
    grade = models.PositiveIntegerField(choices=choices_rate, verbose_name='امتیاز')
    stars = models.CharField(default=0, max_length=5)
    stars_left = models.CharField(blank=True, max_length=5)
    products = models.ManyToManyField(Product, blank=True, verbose_name='کالا')

    def jpublish(self):
        return jalali_converter(self.date_posted)


class contact_with_us(models.Model):
    user = models.ForeignKey(to='user_auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    content = models.TextField()
    def __str__(self):
        return self.user.mobile+" "+self.name


class Comment_shop(models.Model):
    feedbacker = models.ForeignKey(to='user_auth.User', on_delete=models.CASCADE, blank=True, null=True,verbose_name='نظر دهنده')
    content = models.TextField(verbose_name='محتوای کامنت')
    date_posted = models.DateTimeField(default=timezone.now, verbose_name='زمان پست کامنت')
    grade = models.PositiveIntegerField(choices=choices_rate, verbose_name='امتیاز کامنت')
    stars = models.CharField(default=0, max_length=5)
    stars_left = models.CharField(blank=True, max_length=5)
    shop = models.ManyToManyField(myshop, blank=True)

    def jpublish(self):
        return jalali_converter(self.date_posted)


class ticket(models.Model):
    title = models.CharField(max_length=50,verbose_name="عنوان تیکت")
    user = models.ForeignKey(to='user_auth.User', on_delete=models.CASCADE)
    question = models.TextField(verbose_name="سوال شما")
    answer = models.TextField(blank=True)
    is_answerd = models.BooleanField(default=False)
    date_posted = models.DateTimeField(default=timezone.now)
    def jpublish(self):
        return jalali_converter(self.date_posted)

    def __str__(self):
        return self.user.mobile+" "+self.title