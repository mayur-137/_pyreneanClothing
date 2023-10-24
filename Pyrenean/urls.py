from django.urls import path
from Pyrenean.views import HomeView, AboutView, ContactView, CartView, ProductDetailsView, ContactFormView, \
     CustomerServiceView, AddToCartView, Update_cart_view, RemoveItemView, LoginView, RegisterView, ResetView, UserData, Rozor
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
    
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", views.logout_request, name="logout"),
    
    path("register_verified/", views.register_verified, name="register_verified"),
    path("forget_password/", views.forget_password, name="register_verified"),
    path("reset_verified/", views.reset_verified, name="reset_verified"),
    path("reset_password/", ResetView.as_view(), name="reset_passsowrd"),
    path("forget_username/", views.forget_username, name="forget_username"),

    path('edit_user_data/',views.UserData.edit_user_data, name="edit_user_data"),
    path("user_data/", UserData.user_data_function, name="user_data"),
    
    # path('edit_user_data/', views.edit_user_data, name="edit_user_data"),
    path('customerService/', CustomerServiceView.as_view(), name="customerService"),
    path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('updateCart/', Update_cart_view.as_view(), name="update cart"),
    path('removeItem/', RemoveItemView.as_view(), name='removeItem'),

    path('initiate_payment/', Rozor.homepage, name="initiate_payment"),
    path('initiate_payment/paymenthandler/', Rozor.paymenthandler, name='paymenthandler'),

    path('TermsConditions/',views.terms_conditions, name='TermsConditions'),
    path('handlerequest/',views.paytm_payment.handlerequest, name='handlerequest'),

]
