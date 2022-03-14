from django.urls import path
from blog.views import home, contact, my_tickets, profile, search, about_us, category, supcategory
from shop.views import help_video


urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('myticket/', my_tickets, name='my_ticket'),
    path('profile/', profile, name='my_profile'),
    path('about/', about_us, name='about'),
    path('search/', search, name='search'),
    path('category/<int:pk>', category, name='category'),
    path('supcategory/<int:pk>', supcategory, name='sup-category'),
    path('help/', help_video, name='help'),

]
