from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('forgot-password',  views.forgot_password, name = "forgot password"),
    path('change-password',  views.change_password, name = "forgot password"),
    path('googlelogin', views.google_login, name = 'google-login'),
    path('callback', views.google_callback, name = 'google-callback'),
    path('activity', views.activity, name = "activity_page"),
    path('info', views.info, name = "info_page"),
    path('contact', views.contact, name = "contact_page"),
    path('home', views.home, name="home"),
]