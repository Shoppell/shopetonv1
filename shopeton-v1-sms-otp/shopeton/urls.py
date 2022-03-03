from django.contrib import admin
from django.urls import path, include
from . import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from blog.views import  go_to_gateway_shop, callback_gateway_shop
from azbankgateways.urls import az_bank_gateways_urls
admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('', include('shop.urls')),
    path('', include('user_auth.urls')),
    path('bankgateways/', az_bank_gateways_urls()),
    path('go-to-shop/', go_to_gateway_shop, name='go-to-shop'),
    path('callback_shop/', callback_gateway_shop, name='callback-shop'),
]

handler404 = "shop.views.page_404"
handler400 = "shop.views.page_400"
# handler500 = "shop.views.page_500"
handler403 = "shop.views.page_403"
handler_404 = "blog.views.page_404"
handler_400 = "blog.views.page_400"
handler_500 = "blog.views.page_500"
handler_403 = "blog.views.page_403"

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
