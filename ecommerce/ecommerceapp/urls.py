from django.urls import path
from ecommerceapp import views

urlpatterns = [
       path('', views.index,name="index"),
       path('contact', views.contact,name="contact"),
       path('about', views.about,name="about"),
       #path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
        path('cart/', views.view_cart, name='view_cart'),
         path('checkout/', views.checkout, name='checkout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-fail/', views.payment_fail, name='payment_fail'),
    path('payment-cancel/', views.payment_cancel, name='payment_cancel'),

]