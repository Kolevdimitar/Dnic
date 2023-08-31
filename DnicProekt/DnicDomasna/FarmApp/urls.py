from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from .views import landing_page, menu_page, product_list, shopping_cart, checkout_page, payment_page, add_to_cart

urlpatterns = [
    path('',landing_page,name='landing-page'),
    path('menu/',menu_page,name='menu-page'),
    path('list/',product_list,name='product-list'),
    path('cart/',shopping_cart,name='shopping-cart'),
     path('checkout/',checkout_page,name='checkout'),
    path('payment/',payment_page,name='payment'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart')
]