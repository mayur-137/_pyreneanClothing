from django.views.generic.base import TemplateView
from django.http import HttpResponse, Http404
from django.views.generic.edit import CreateView
from .models import Mens, Women, Kid, ContactModel, user_data, CartModel
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm  # add this
from django.contrib.auth import login, authenticate, logout  # add this
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactFormModel, NewUserForm, ProductBuyFormDetails
from django.contrib.auth.models import User, auth
from django.views import View
from django.contrib.auth.decorators import login_required

global product_total


class HomeView(TemplateView):
    template_name = "Home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Mens"] = Mens.objects.all()
        context["Kids"] = Kid.objects.all()
        context["Women"] = Women.objects.all()
        return context


class AboutView(TemplateView):
    template_name = "About.html"

    def get_context_data(self, **kwargs):
        about = super().get_context_data()
        return about


class ContactView(TemplateView):
    template_name = "Contact.html"

    def get_context_data(self, **kwargs):
        contact = super().get_context_data()
        return contact


class ContactFormView(CreateView):
    model = ContactModel
    form_class = ContactFormModel
    template_name = "Contact.html"
    success_url = "/contact/"

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ProductDetailsView(TemplateView):
    model = Mens
    template_name = "Product-Details.html"

    def get_context_data(self, **kwargs):
        VG = super().get_context_data()
        slug = self.kwargs.get("slug")
        VG["PRD"] = Mens.objects.filter(slug=slug)
        if not VG["PRD"]:
            VG["PRD"] = Kid.objects.filter(slug=slug)
        if not VG["PRD"]:
            VG["PRD"] = Women.objects.filter(slug=slug)
        return VG


class CustomerServiceView(TemplateView):
    template_name = "Customer-Service.html"

    def get_context_data(self, **kwargs):
        customerService = super().get_context_data()
        return customerService


class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        models = [Mens, Kid, Women]
        for model in models:
            try:
                product = get_object_or_404(model, id=product_id)
            except Http404:
                pass
        cart_session = request.session.get('cart_session', {})
        cart_session[product_id] = cart_session.get(product_id, 0) + 1
        request.session['cart_session'] = cart_session
        print(request.session['cart_session'], "1")
        print(cart_session, "2")
        return redirect("/cart/")


class CartView(View):
    model = CartModel

    def get(self, request, *args, **kwargs):
        # global product
        products_in_cart = []
        products_list = []
        # products_list.clear()
        product_total = 0
        cart = request.session.get('cart_session', {})
        print(cart, "3")
        models = [Mens, Kid, Women]
        for model in models:
            try:
                itm = model.objects.filter(id__in=cart.keys())
                # print(cart.keys(), "4")
                # print(itm, model, "itm")
                if itm:
                    products_in_cart.append(itm)
                    # print(model, "i am in if")
                # products_in_cart.append(itm)
                # print(products_in_cart, "5")
                # products_in_cart.clear()
            except:
                pass
        for products in products_in_cart:
            # print(products, "products ")
            # print(products_in_cart, "cart==================")
            for product in products:
                # print(product, "6")
                # print(product.price, "price")
                # print(cart[str(product.id)], "quntity")
                product.subtotal = product.price * cart[str(product.id)]
                # print(product.subtotal, "subtotal")
                product_total = product.subtotal + product_total
                # print(product_total, "total")
                product.product_quantity = str(cart[str(product.id)])
                # print(str(cart[str(product.id)]), "str(cart[str(product.id)])")
                products_list.append(product)
            # print(products_list, "list")
        return render(request, 'cart.html', {'products': products_list, 'product_total': product_total})


class Update_cart_view(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.GetMaxQuantity = None

    def post(self, request, *args, **kwargs):
        Product_id = request.POST.get("Update_product_quantity")
        print(Product_id, "ID")
        Mode_of_Operations = request.POST.get("minus")
        if Mode_of_Operations == "-":
            cart_session = request.session.get('cart_session', {})
            cart_session[Product_id] = cart_session.get(Product_id) - 1
            request.session['cart_session'] = cart_session
            if cart_session.get(Product_id) == 0:
                del cart_session[Product_id]
        else:
            models = [Mens, Kid, Women]
            for model in models:
                try:
                    self.GetMaxQuantity = model.objects.filter(id=Product_id).values("max_quantity").get()
                except:
                    pass
            cart_session = request.session.get('cart_session', {})
            if not cart_session.get(Product_id) == self.GetMaxQuantity["max_quantity"]:
                cart_session[Product_id] = cart_session.get(Product_id) + 1
                request.session['cart_session'] = cart_session
        return redirect("/cart/")


class RemoveItemView(View):

    def post(self, request, *args, **kwargs):
        GetRemoveItemId = request.POST.get("removeItem")
        cart_session = request.session.get('cart_session', {})
        models = [Mens, Kid, Women]
        for model in models:
            try:
                product = get_object_or_404(model, id=GetRemoveItemId)
            except Http404:
                pass
        if GetRemoveItemId in cart_session:
            del cart_session[GetRemoveItemId]
            request.session['cart_session'] = cart_session
        return redirect("/cart/")


class LoginView(TemplateView):
    template_name = "registration/login.html"


def user_data_function(request):
    current_user = request.user
    email = current_user.email
    if email:
        try:
            print("user already stored data")
            username = (User.objects.get(email=email)).username
            print(username)
            phone_number = user_data.objects.get(email=email).phone_number
            building = user_data.objects.get(email=email).building
            print(building)
            street = (user_data.objects.get(email=email)).street
            area = (user_data.objects.get(email=email)).area
            pincode = (user_data.objects.get(email=email)).pincode
            city = (user_data.objects.get(email=email)).city
            context = {"email": email, "phone_number": phone_number, 'username': username, 'building': building,
                       'street': street, 'area': area, 'pincode': pincode, 'city': city}
            print(context)
            return render(request, 'user_data.html', {'context': context})

        except:
            return render(request, 'user_data.html')
    else:
        return render(request, 'user_data.html')


def edit_user_data(request):
    print("edit user data")
    if request.method == "POST":
        print("edit user data222")
        current_user = request.user
        email = current_user.email
        building = request.POST['building']
        street = request.POST['street']
        area = request.POST['area']
        pincode = request.POST['pincode']
        city = request.POST['city']
        phone_number = request.POST['phone_number']

        if user_data.objects.filter(email=email).exists():
            print("your data is saved")
            user = user_data.objects.get(email=email)
            user.building = building
            user.street = street
            user.area = area
            user.pincode = pincode
            user.city = city
            user.phone_number = phone_number
            user.save()
        else:
            print("user data is not saved")
            b = user_data(email=email, building=building, street=street, area=area, pincode=pincode, city=city,
                          phone_number=phone_number)
            user_data.save(b)
        return redirect('/')
    else:
        return render(request, 'edit_user_data.html')


@csrf_exempt
def register_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        print(username, email, password)
        if User.objects.filter(username=username).exists():
            print("user already registered")
            context = {'error': 'The username you entered has already been taken. Please try another username.'}
            return render(request, 'register.html', {'context': context})
        elif User.objects.filter(email=email).exists():
            print("this email is already taken try another one")
            context = {"error": "this email is already taken try another one"}
            return render(request, 'register.html', {"context": context})
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            print("user created")
            # context = {'error': 'User registered successfully!'}
            return redirect('main:login')
    else:
        print("noooo")
        return render(request, 'register.html')

    # return render (request=request, template_name="main/register.html", context={"register_form":form})


@csrf_exempt
def login_request(request):
    if request.method == "POST":
        email = request.POST['email_address']
        password = request.POST['password']
        try:
            username = User.objects.get(email=email)
            print("email--", email, "password--", password, "username--", username.email)
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                print("user logged in")
                return redirect('/')
            else:
                context = {'error': 'email and password does not match.'}
                return render(request, 'login.html', {'context': context})
        except:
            context = {'error': 'user not found go to register'}
            return render(request, 'login.html', {'context': context})
    else:
        return render(request, 'login.html')


@csrf_exempt
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")
