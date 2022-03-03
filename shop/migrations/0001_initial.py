# Generated by Django 4.0.2 on 2022-02-25 16:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='myshop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='اسم فروشگاه')),
                ('head_title', models.CharField(max_length=100, verbose_name='عنوان سر تیتر')),
                ('head_description', models.CharField(max_length=80, verbose_name='توضیحات سر تیتر')),
                ('head_link', models.TextField(blank=True, verbose_name='لینک تیتر')),
                ('image_head1', models.ImageField(upload_to='shops.head', verbose_name='عکس تیتر اول')),
                ('slug', models.SlugField(unique=True, verbose_name='آیدی فروشگاه شما')),
                ('phone', models.CharField(max_length=30, verbose_name='تلفن شما')),
                ('phone_bool', models.BooleanField(default=False, verbose_name='تلفن شما نمایش داده شود؟')),
                ('address', models.TextField(verbose_name='آدرس شما')),
                ('address_bool', models.BooleanField(default=False, verbose_name='آدرس شما نمایش داده شود؟')),
                ('why_us1', models.CharField(max_length=50, verbose_name='عنوان اول چرا ما')),
                ('why_us2', models.CharField(max_length=50, verbose_name='عنوان دوم چرا ما')),
                ('why_us3', models.CharField(max_length=50, verbose_name='عنوان سوم چرا ما')),
                ('image_banner1', models.ImageField(upload_to='shops.banner', verbose_name='عکس بنر اول')),
                ('image_banner2', models.ImageField(upload_to='shops.banner', verbose_name='عکس بنر دوم')),
                ('image_banner3', models.ImageField(upload_to='shops.banner', verbose_name='عکس بنر سوم')),
                ('image_look', models.ImageField(upload_to='shops.look', verbose_name='عکس پوستر')),
                ('title_look', models.CharField(max_length=50, verbose_name='عنوان پوستر')),
                ('description_look', models.TextField(verbose_name='توضیحات پوستر')),
                ('h_index', models.IntegerField(default=0, verbose_name='رتبه ی فروشگاه')),
                ('grade', models.PositiveIntegerField(default=0, verbose_name='رتبه بر اساس نظرات')),
                ('stars', models.CharField(default=0, max_length=5)),
                ('stars_left', models.CharField(blank=True, max_length=5)),
                ('verified', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('time_created', models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='زمان ساخت فروشگاه')),
                ('seller_info', models.CharField(max_length=150, verbose_name='مشتری از کجا محصول شما رو خریداری کند؟(برای تمام محصولات اعمال میشود)')),
                ('about', models.TextField(verbose_name='درباره ی فروشگاه')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.PositiveIntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('paid', models.BooleanField(default=False, verbose_name='پرداخت شده؟')),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='postinfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('family_name', models.CharField(max_length=200)),
                ('address', models.TextField()),
                ('postal_code', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=20)),
                ('time_add', models.DateTimeField(default=django.utils.timezone.now, verbose_name='زمان اضافه شدن')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام کالا')),
                ('photo', models.ImageField(upload_to='products', verbose_name='عکس اول کالا')),
                ('photo_2', models.ImageField(blank=True, upload_to='products', verbose_name='عکس دوم کالا')),
                ('photo_3', models.ImageField(blank=True, upload_to='products', verbose_name='عکس سوم کالا')),
                ('photo_4', models.ImageField(blank=True, upload_to='products', verbose_name='عکس چهارم کالا')),
                ('photo_5', models.ImageField(blank=True, upload_to='products', verbose_name='عکس پنجم کالا')),
                ('photo_6', models.ImageField(blank=True, upload_to='products', verbose_name='عکس ششم کالا')),
                ('price', models.IntegerField(verbose_name='قیمت کالا| بدون تخفیف')),
                ('off', models.PositiveIntegerField(verbose_name='تخفیف')),
                ('details', models.TextField(verbose_name='درباره ی کالا')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت کالا')),
                ('hot', models.BooleanField(default=False, verbose_name='کالا داغ است؟')),
                ('most_off', models.BooleanField(default=False, verbose_name='کالا پر تخفیف است؟')),
                ('rare', models.BooleanField(default=False, verbose_name='کالا بسیار ویژه است؟')),
                ('in_stock', models.BooleanField(default=True, verbose_name='کالا موجود است؟')),
                ('star_rate', models.PositiveIntegerField(blank=True, default=0)),
                ('stars', models.CharField(default=0, max_length=5)),
                ('stars_left', models.CharField(blank=True, max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid', models.BooleanField(default=False, verbose_name='پرداخت شده؟')),
                ('time_add', models.DateTimeField(default=django.utils.timezone.now, verbose_name='زمان اضافه شدن')),
                ('status', models.CharField(blank=True, choices=[('کالا در حال آماده سازی برای ارسال است', 'کالا در حال آماده سازی برای ارسال است'), ('کالا تحویل پست داده شد', 'کالا تحویل پست داده شد')], max_length=100, null=True, verbose_name='وضعیت ارسال کالا')),
            ],
        ),
    ]