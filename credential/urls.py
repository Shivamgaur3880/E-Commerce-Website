from django.contrib import admin
from django.urls import path,include
from credential import views

urlpatterns = [
    path('signup/', views.signup),
    path('login/',views.handlelogin),
    path('logout/',views.handlelogout),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),

]