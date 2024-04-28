from django.urls import path
from . import views

urlpatterns = [
    path("",views.login, name="login"),
    path("register/",views.register, name="register"),
    path("home/",views.home, name="home"),
    path("home/cart/",views.cart, name="cart"),
    path('update_item/', views.updateItem, name="update_item"),
    path('home/cart/checkout',views.checkout, name="checkout"),
    path('restaurant/cart/payment',views.payment, name="payment"),
    path('home/profile/', views.profile, name='profile'),
    path('home/profile/logout', views.logout, name='logout'),
    path("chef_panel/", views.chef_panel, name="chef_panel"),
    path("chef_panel/update_status/", views.update_status, name="update_status"),
]
