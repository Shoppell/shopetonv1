from django.urls import path
from user_auth.views import verify, register_view
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('verify/', verify, name='verify'),
    path('register/', register_view, name='register'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),

]
