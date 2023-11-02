from django.urls import path
from Pyrenean.views import (HomeView, AboutView, ContactView, CartView, ProductDetailsView, ContactFormView, \
                            CustomerServiceView, AddToCartView, Update_cart_view, RemoveItemView, LoginView,
                            RegisterView, ResetView, Rozor, WishListView, WishListAddView, RemoveWishListItem,
                            SubscribeView,Terms_ConditionView, TestView, PromoCodeView,razor_payment, VerifyOTPView,
                            forget_password, reset_verified, forget_username, ProfileView, EditProfileView)
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

    path("register_verified/", VerifyOTPView.as_view(), name="register_verified"),
    path("forget_password/", forget_password.as_view(), name="register_verified"),
    path("reset_verified/", reset_verified.as_view(), name="reset_verified"),
    path("reset_password/", ResetView.as_view(), name="reset_passsowrd"),
    path("forget_username/", forget_username.as_view(), name="forget_username"),

    # path('edit_user_data/', views.UserData.edit_user_data, name="edit_user_data"),
    # path("user_address/", UserData.user_data_function, name="user_address"),

    path("profile/", ProfileView.as_view(), name="profile"),
    path("EditProfile/", EditProfileView.as_view(), name="editProfile"),

    # path('edit_user_data/', views.edit_user_data, name="edit_user_data"),
    path('customerService/', CustomerServiceView.as_view(), name="customerService"),
    path('Terms_Condition/', Terms_ConditionView.as_view(), name="Terms_ConditionView"),
    path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('updateCart/', Update_cart_view.as_view(), name="update cart"),
    path('removeItem/', RemoveItemView.as_view(), name='removeItem'),

    path('initiate_payment/', Rozor.homepage, name="initiate_payment"),
    # path('initiate_payment/paymenthandler/', Rozor.paymenthandler, name='paymenthandler'),
    #
    path("COD/",razor_payment.Cash_on_delivery,name="Cash on delivery"),
    # path("cashfree/", Rozor.cashfree_dashboard,name="cashfree"),
    # path("cashfree_handle/", Rozor.cashfree_handle, name="cashfree_handle"),

]
