from django.urls import path
from Pyrenean.views import HomeView, AboutView, ContactView, CartView, ProductDetailsView, ContactFormView, \
     CustomerServiceView, AddToCartView, Update_cart_view, RemoveItemView
from . import views

app_name = "main"

urlpatterns = [
    path('', HomeView.as_view(), name="index"),
    path('about/', AboutView.as_view(), name="about"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('cart/', CartView.as_view(), name="cart"),
    path('submit/', ContactFormView.as_view(), name="submit"),
    path('ProductDetails/<slug:slug>', ProductDetailsView.as_view(), name="ProductDetails"),
    path('ProductDetails/<slug:slug>/<str:size>/<str:id>', ProductDetailsView.as_view(), name="ProductDetails"),
    
    path("register/", views.login_register.register_request, name="register"),
    path("login/", views.login_register.login_request, name="login"),
    path("logout/", views.login_register.logout_request, name= "logout"),
    
    path("register_verified/", views.reset.register_verified, name= "register_verified"),
    path("forget_password/", views.reset.forget_password, name= "register_verified"),
    path("reset_verified/", views.reset.reset_verified, name= "reset_verified"),
    path("reset_password/", views.reset.reset_passsowrd, name= "reset_passsowrd"),
    path("forget_username/", views.reset.forget_username, name= "forget_username"),

    path('edit_user_data/',views.user_datas.edit_user_data,name="edit_user_data"),
    path("user_data/", views.user_datas.user_data_function, name= "user_data"),
    



    # path('edit_user_data/', views.edit_user_data, name="edit_user_data"),
    path('customerService/', CustomerServiceView.as_view(), name="customerService"),
    path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('updateCart/', Update_cart_view.as_view(), name="update cart"),
    path('removeItem/', RemoveItemView.as_view(), name='removeItem'),



]
