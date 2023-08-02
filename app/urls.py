from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    
    path('home',views.home,name="home"),
    path('',views.userlogin,name="login"),
    path('register',views.register,name="register"),
    path('logout',views.userlogout,name="logout"),
    path('contact',views.contact,name="contact"),
    path('profile',views.profile,name="profile"),
    path('address',views.address,name="address"),
    path('cart/',views.show_cart,name="showcart"),
    path('invoice/<int:pk>',views.invoice,name="invoice"),
    path('orders',views.orders,name="orders"),
    path('add-to-cart/',views.add_to_cart,name="add-to-cart"),
    path('deletecartitem/<int:pk>',views.deletecartitem,name="deletecartitem"),
    path('checkout',views.checkout.as_view(),name="checkout"),

    
    path('deleteaddress/<int:pk>',views.deleteaddress,name="deleteaddress"),
    path('updateaddress/<int:pk>',views.updateaddress,name="updateaddress"),
    path('category/<slug:val>',views.category.as_view(),name="category"),
    path('productdetails/<int:pk>',views.productdetails.as_view(),name="productdetails"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  
