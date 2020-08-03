from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('register',views.register),
    path('confirmEmail',views.confirmEmail),
    path('confirmPhone',views.confirmPhone),
    path('confirm',views.confirm,name='confirm'),
    path('profile',views.profile,name='profile'),
    path('logout',views.logout,name='logout'),
    path('verifylogin',views.verifylogin),
    path('login',views.login),
path('phone',views.phone,name='phone'),
path('email',views.email,name='email')

]