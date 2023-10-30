from django.urls import path
from Pyrenean.views import (HomeView, AboutView, ContactView, CartView, ProductDetailsView, ContactFormView, \
                            CustomerServiceView, AddToCartView, Update_cart_view, RemoveItemView, LoginView,
                            RegisterView, ResetView, UserData, Rozor, WishListView, WishListAddView, RemoveWishListItem, SubscribeView,
                            Terms_ConditionView, TestView, PromoCodeView,razor_payment)
from . import views

app_name = "main"

urlpatterns = [
    path('', HomeView, name="index"),
    path('test/', TestView.as_view(), name="test"),
    path('about/', AboutView.as_view(), name="about"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('cart/', CartView.as_view(), name="cart"),
    path('wishlist/', WishListView.as_view(), name="wishlist"),
    path('WishListAddView/', WishListAddView.as_view(), name="WishListAddView"),
    path('removeWishListItem/', RemoveWishListItem.as_view(), name="removeWishListItem"),
    path('contactForm/', ContactFormView.as_view(), name="submit"),
    path('Subscribe/', SubscribeView.as_view(), name="SubscribeView"),
    path('ProductDetails/<slug:slug>', ProductDetailsView.as_view(), name="ProductDetails"),
    path('ProductDetails/<slug:slug>/<str:size>/<str:id>', ProductDetailsView.as_view(), name="ProductDetails"),
    path('PromoCode/', PromoCodeView.as_view(), name="PromoCode"),

    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", views.logout_request, name="logout"),

    path("register_verified/", views.register_verified, name="register_verified"),
    path("forget_password/", views.forget_password, name="register_verified"),
    path("reset_verified/", views.reset_verified, name="reset_verified"),
    path("reset_password/", ResetView.as_view(), name="reset_passsowrd"),
    path("forget_username/", views.forget_username, name="forget_username"),

    path('edit_user_data/', views.UserData.edit_user_data, name="edit_user_data"),
    path("user_address/", UserData.user_data_function, name="user_address"),

    # path('edit_user_data/', views.edit_user_data, name="edit_user_data"),
    path('customerService/', CustomerServiceView.as_view(), name="customerService"),
    path('Terms_Condition/', Terms_ConditionView.as_view(), name="Terms_ConditionView"),
    path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('updateCart/', Update_cart_view.as_view(), name="update cart"),
    path('removeItem/', RemoveItemView.as_view(), name='removeItem'),

    path('initiate_payment/', Rozor.homepage, name="initiate_payment"),
    path('initiate_payment/paymenthandler/', Rozor.paymenthandler, name='paymenthandler'),
    #
    path("cashfree/",razor_payment.cashfree_dashboard,name="cashfree"),
    path("cashfree_handle/",razor_payment.cashfree_handle, name="cashfree_handle"),

]
