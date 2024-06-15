from django.urls import path
from .views import *

urlpatterns = [
    path('',Index,name='Index'),
    path('About/',About,name='About'),
    path('AddProduct/',AddProduct,name='AddProduct'),
    path('Productdata/',Productdata,name='Productdata'),
    path('Product/',allProduct,name='Product'),
    path('Delete/<int:pk>',Delete,name='Delete'),
    path('AddToCart/<int:pk>',AddToCart,name='AddToCart'),
    path('Cart/',Cart,name='Cart'),
    path('Payment/',Payment,name='Payment'),
    path('payment-status', payment_status, name='payment-status'),
    path('Contact/',Contact,name='Contact'),
    path('Registerdata/',Registerdata,name='Registerdata'),
    path('Register/',Register,name='Register'),
    path('logindata/',LoginData,name='logindata'),
    path('Login/',Login,name='Login'),
    path('Logout/',Logout,name='Logout')
]
