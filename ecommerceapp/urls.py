from django.contrib import admin
from django.urls import path,include
from ecommerceapp import views

urlpatterns = [
    
    path('',views.index,name="home"),
    path('contact',views.contact,name="contact"),
    path('about',views.about,name="about"),
    path('feedback',views.feedback),
    path('profile/',views.profile,name="profile"),
    path('checkout/',views.checkout,name="checkout"),
    path('handlerequest/', views.handlerequest, name="HandleRequest"),
]