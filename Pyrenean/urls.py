from django.urls import path
from Pyrenean.views import HomeView, AboutView, ContactView, CartView, ProductDetailsView, ContactFormView, \
    edit_user_data, CustomerServiceView, AddToCartView, Update_cart_view, RemoveItemView
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
    path("user_data/", views.user_data_function, name="user_data"),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path('edit_user_data/', views.edit_user_data, name="edit_user_data"),
    path('customerService/', CustomerServiceView.as_view(), name="customerService"),
    path('add_to_cart/', AddToCartView.as_view(), name='add_to_cart'),
    path('updateCart/', Update_cart_view.as_view(), name="update cart"),
    path('removeItem/', RemoveItemView.as_view(), name='removeItem'),



]
