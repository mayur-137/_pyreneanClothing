import ast
import json
import random
import razorpay
import requests
import datetime
from datetime import timedelta,datetime
from math import ceil
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib.auth.models import User, auth
from django.db.models import Max
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.core.mail import EmailMessage

from .forms import ContactFormModel, SubscribeForm
from .models import ContactModel, user_address, Product_Details, Size, user_email, cart_data, final_order, WishList, \
    SubscribeNow, PromoCode

from .configurations import email_content

global product_total, slug, discounted_price_coupen, discount_coupen, promo_code,current_time
current_datetime = datetime.now()
# Format the current datetime as a string in the desired format
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")



def HomeView(request):
    return render(request, "Comming-Soon.html")


class TestView(TemplateView):
    template_name = "Home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Products"] = Product_Details.objects.all()
        context['Size'] = Size.objects.all()
        for data in context["Products"]:
            data.discounted_price = ceil(data.price - (data.price * data.discount / 100))
        return context


class AboutView(TemplateView):
    template_name = "About.html"

    def get_context_data(self, **kwargs):
        about = super().get_context_data()
        return about


class MailView(View):
    email = "Pyrenean Clothing <info@pyreneanclothing.com>"
    signature = "\n\nBest Regards,\nPyrenean Clothing"

    def send_email(self, subject, message, to_email):
        message += self.signature
        email = EmailMessage(subject, message, self.email, [to_email])
        print(subject, message, self.email, to_email, "contact")
        email.send()

    @staticmethod
    def OtpGeneration():
        print("generate otp")
        OTP = random.randint(100000, 999999)
        print(OTP)
        return OTP

    @staticmethod
    def Verification(request, email, user_otp):
        print(user_otp, email, "verification")
        resetpassword_opt = request.session.get("otp")
        try:
            user = user_email.objects.get(email=email)
            otp = user.otp
        except Exception as e:
            print(e, "eee1")

        if int(user_otp) == int(resetpassword_opt):
            return True
        else:
            return False

    def Store_otp(self, email, otp):
        if user_email.objects.filter(email=email).exists():
            user = user_email.objects.get(email=email)
            user.email = email
            user.otp = otp
            user.save()
        else:
            b = user_email(email=email, otp=otp)
            user_email.save(b)


class ContactView(TemplateView):
    template_name = "Contact.html"

    def get_context_data(self, **kwargs):
        contact = super().get_context_data()
        return contact


class ContactFormView(CreateView, MailView):
    model = ContactModel
    form_class = ContactFormModel
    template_name = "Contact.html"
    success_url = "/contact/"

    def form_valid(self, form):
        contact = super().form_valid(form)
        email = form.cleaned_data["email"]
        message = form.cleaned_data["message"]
        contact_email_json = email_content.email_content
        contact_email_json_subject = contact_email_json["contact_us"]["subject"]
        contact_email_json_body = contact_email_json["contact_us"]["body"]
        message = message + contact_email_json_body
        self.send_email(contact_email_json_subject, message, email)
        return contact

    def form_invalid(self, form):
        contact = super().form_invalid(form)
        print("no not submit")
        return contact


class ProductDetailsView(TemplateView):
    template_name = "Product-Details.html"

    def get_context_data(self, **kwargs):
        PD = super().get_context_data()
        slug = self.kwargs.get("slug")
        PD["size"] = self.kwargs.get("size")
        PD["size_id"] = self.kwargs.get("id")
        PD['Size'] = Size.objects.all()
        PD["slug"] = self.kwargs.get("slug")
        PD["PRD"] = Product_Details.objects.filter(slug=slug)
        for data in PD['PRD']:
            if data.discount != 0:
                data.discounted_price = ceil(data.price - (data.price * data.discount / 100))
        return PD


class CustomerServiceView(TemplateView):
    template_name = "Customer-Service.html"

    def get_context_data(self, **kwargs):
        customerService = super().get_context_data()
        return customerService


class AddToCartView(View):

    def post(self, request, *args, **kwargs):
        print("add to cart")
        getSize_id = request.POST.get("size_id")
        print("size is", getSize_id, type(getSize_id))

        if getSize_id == str(None):
            print("select size you idiot")
            slug = request.POST.get("slug")
            messages.error(request, "Please select a size first")
            print("redirecting", slug)
            return redirect(f"/ProductDetails/{slug}")

        else:
            print("size is selected")
            product_id = request.POST.get('product_id')
            getSize_id = request.POST.get("size_id")
            getSize_id = getSize_id.split("=")[1]
            size_session = request.session.get("size_session", {})
            product = Size.objects.filter(id=getSize_id)
            print("size is ", getSize_id, size_session)
            for detail in product:
                pass

            if size_session.get(getSize_id) is None or size_session.get(getSize_id) < detail.quantity:
                size_session[getSize_id] = size_session.get(getSize_id, 0) + 1
                request.session["size_session"] = size_session

            return redirect("/cart/")


class CartView(View):

    def get(self, request, *args, **kwargs):

        global discounted_price_coupen, discount_coupen, promo_code
        products_in_cart = []
        order_product_data = []
        products_list = []
        product_total = 0
        size_session = request.session.get("size_session", {})
        try:
            discount_coupen = request.session["discount_coupen"]
            discounted_price_coupen = request.session["discounted_price"]
            promo_code = request.session["PromoMessage"]
            print(discount_coupen, discounted_price_coupen, promo_code, "hey")
        except Exception as e:
            discount_coupen = 0
            discounted_price_coupen = 0
            promo_code = 0
            print(e, "Promo error")
        try:
            itm = Size.objects.filter(id__in=size_session.keys())
            if itm:
                products_in_cart.append(itm)
        except:
            pass
        for products in products_in_cart:
            for product in products:
                try:
                    product.discounted_price = ceil(
                        product.product.price - (product.product.price * product.product.discount / 100))
                    product.subtotal = product.discounted_price * size_session[str(product.id)]
                    product_total = product.subtotal + product_total
                    product_size = product.size
                    product.product_quantity = str(size_session[str(product.id)])
                    product_in_cart = {"product_id": str(product.product.id), "price": product.discounted_price,
                                       "quantity": product.product_quantity,
                                       "size": product.size, "size_id": str(product.id), "subtotal": product.subtotal}
                    
                    # product_in_cart = str(product.product.id) + "#" + str(product.discounted_price) +"#"+ str( product.product_quantity) + "#"+ str(product.size)
                    
                    product_in_cart_Json = json.dumps(product_in_cart)
                    order_product_data.append(product_in_cart_Json)
                    products_list.append(product)
                except Exception as e:
                    continue

        user = request.user
        if not user.is_authenticated:
            messages.error(request, "Please Login or Register First")
            return redirect("/register/")

        email = request.user.email
        if cart_data.objects.filter(email=email).exists():
            if order_product_data != "":
                users = cart_data.objects.get(email=email)
                users.products_detail = order_product_data
                users.order_total = product_total
                users.save()

            user_cart_fill = cart_data.objects.filter(email=email)
            for i in user_cart_fill:
                f = []
                for j in i.products_detail:
                    JsonExtractedData = json.loads(j)
                    GetPrice = JsonExtractedData["price"]
                    GetSize = JsonExtractedData["size"]
                    GetSize_id = JsonExtractedData["size_id"]
                    GetQuantity = JsonExtractedData["quantity"]
                    Getsubtotal = JsonExtractedData["subtotal"]
                    getDataForCart = Product_Details.objects.filter(id=JsonExtractedData["product_id"])
                    for getDataForCartEdit in getDataForCart:
                        getDataForCartEdit.price = GetPrice
                        getDataForCartEdit.size = GetSize
                        getDataForCartEdit.size_id = GetSize_id
                        getDataForCartEdit.quantity = GetQuantity
                        getDataForCartEdit.subtotal = Getsubtotal
                        f.append(getDataForCartEdit)
                    if discounted_price_coupen == 0:
                        discounted_price_coupen = i.order_total
                    elif i.order_total < 1500:
                        discount_coupen = 0
                        discounted_price_coupen = i.order_total
                    else:
                        pass
                return render(request, 'cart_checkout/Cart.html',
                              {'products': f, 'product_total': i.order_total, "discount": discount_coupen,
                               "discounted_price": discounted_price_coupen, "PromoMessage": promo_code})
            else:
                user_cart_fill = cart_data.objects.filter(email=email)
                for i in user_cart_fill:
                    f = []
                    for j in i.products_detail:
                        JsonExtractedData = json.loads(j)
                        GetPrice = JsonExtractedData["price"]
                        GetSize = JsonExtractedData["size"]
                        GetSize_id = JsonExtractedData["size_id"]
                        GetQuantity = JsonExtractedData["quantity"]
                        Getsubtotal = JsonExtractedData["subtotal"]
                        getDataForCart = Product_Details.objects.filter(id=JsonExtractedData["product_id"])
                        for getDataForCartEdit in getDataForCart:
                            getDataForCartEdit.price = GetPrice
                            getDataForCartEdit.size = GetSize
                            getDataForCartEdit.size_id = GetSize_id
                            getDataForCartEdit.quantity = GetQuantity
                            getDataForCartEdit.subtotal = Getsubtotal
                            f.append(getDataForCartEdit)

                    return render(request, 'cart_checkout/Cart.html',
                                  {'products': f, 'product_total': i.order_total})
        else:
            if order_product_data != "":
                print(order_product_data, "data111")
                b = cart_data(email=email, products_detail=order_product_data,order_total=product_total)
                cart_data.save(b)
                return render(request, 'cart_checkout/Cart.html',
                              {'products': products_list, 'product_total': product_total})
            else:
                messages.info(request, "Please Choose the Product First")
                return redirect("/")
        return render(request, 'cart_checkout/cart.html',
                      {'products': products_list, 'product_total': product_total})


class WishListAddView(View):

    def post(self, request, *args, **kwargs):
        favitem_id = request.POST.get("Favitem")
        try:
            addFavItem = WishList(product_id=favitem_id).save()
        except Exception as e:
            print(e)
        return redirect("/wishlist/")


class WishListView(View):

    def get(self, request, *args, **kwargs):
        try:
            FavList = []
            getFavItem = WishList.objects.all()
            print(getFavItem, "fav")
            for item in getFavItem:
                print(item.product_id, "fav item")
                favitem = Product_Details.objects.filter(id=item.product_id)
                for data in favitem:
                    print(data.price, "data")
                    data.discounted_price = ceil(data.price - (data.price * data.discount / 100))

                FavList.append(data)
                print(FavList, "list")
            return render(request, "wishlist.html", {"FV": FavList})

        except Exception as e:
            print(e)


class RemoveWishListItem(View):

    def post(self, request, *args, **kwargs):
        RemoveWishItem_id = request.POST.get("removeWishListItem")
        try:
            addFavItem = WishList.objects.filter(product_id=RemoveWishItem_id).delete()
        except Exception as e:
            print(e)
        return redirect("/wishlist/")


class Update_cart_view(View):

    def post(self, request, *args, **kwargs):
        Size_id = request.POST.get("Update_product_quantity")
        Mode_of_Operations = request.POST.get("minus")
        size_session = request.session.get("size_session", {})

        product = Size.objects.filter(id=Size_id)

        for detail in product:
            print(detail.quantity)
        if Mode_of_Operations == "-":
            size_session[Size_id] = size_session.get(Size_id) - 1
            request.session['size_session'] = size_session
            if size_session.get(Size_id) == 0:
                del size_session[Size_id]
        else:
            if not size_session.get(Size_id) == detail.quantity:
                size_session[Size_id] = size_session.get(Size_id) + 1
                request.session['size_session'] = size_session
            else:
                pass
        return redirect("/cart/")


class RemoveItemView(View):

    def post(self, request, *args, **kwargs):
        GetRemoveItemId = request.POST.get("removeItem")
        cart_session = request.session.get('cart_session', {})
        size_session = request.session.get("size_session", {})
        if GetRemoveItemId in size_session:
            del size_session[GetRemoveItemId]
            request.session["size_session"] = size_session
            request.session["discount_coupen"] = 0
            request.session["discounted_price"] = 0
            request.session["PromoMessage"] = None

        print(size_session, cart_session, "sessions")
        return redirect("/cart/")


class SubscribeView(CreateView, MailView):
    model = SubscribeNow
    form_class = SubscribeForm
    template_name = "About.html"
    success_url = "/about/"

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        subscribe_email_json = email_content.email_content
        subscribe_email_json_subject = subscribe_email_json["subscribe"]["subject"]
        subscribe_email_json_body = subscribe_email_json["subscribe"]["body"]
        message = f"""Dear {email}, \n
        {subscribe_email_json_body}
        """
        self.send_email(subscribe_email_json_subject, message, email)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class PromoCodeView(View):
    model = PromoCode
    template_name = "cart_checkout/Cart.html"

    def post(self, request, *args, **kwargs):
        All_promos = PromoCode.objects.all()
        GetPromo = request.POST.get("code")
        GetDiscount = int(request.POST.get("discount_coupen"))
        print(GetDiscount, "id")
        print(GetPromo, "123")
        for promo in All_promos:
            try:
                print(type(GetPromo), type(promo.code))
                if GetPromo == promo.code:
                    print("yes")
                    if int(GetDiscount) >= 1500:
                        discounted_price_coupen = GetDiscount - promo.discount_percent
                        request.session["discount_coupen"] = promo.discount_percent
                        request.session["discounted_price"] = discounted_price_coupen
                        request.session["PromoMessage"] = f"Congratulations, Your Coupon Code {promo.code} Applied."
                        print(request.session["discounted_price"], request.session["discount_coupen"], "0")
                        return redirect("/cart/")
                    else:
                        print(f"not applied because your price is {GetDiscount} less then 1500")
                        request.session[
                            "PromoMessage"] = f"Your Coupon Code Not Applied, Add {1500 - GetDiscount} to Applied."
                        print("1")
                        return redirect("/cart/")
                else:
                    request.session["discount_coupen"] = 0
                    request.session["discounted_price"] = 0
                    request.session["PromoMessage"] = None
                    print("21")
            except Exception as e:
                print(e, "set promo")

        return redirect("/cart/")


class Terms_ConditionView(TemplateView):
    template_name = "terms_conditions.html"

    def get_context_data(self, **kwargs):
        Terms = super().get_context_data()
        return Terms


class mail:

    def confirm_order_mail(self, email):
        order_id = final_order.objects.aggregate(Max('order_id'))['order_id__max']
        order_user = final_order.objects.get(order_id=order_id)
        order_total = order_user.order_total
        order_address = order_user.address
        order_product = ast.literal_eval(order_user.products_detail)
        msg = ""
        for i in order_product:
            name = i.split("#")[0]
            quantity = i.split("#")[1]
            price = i.split("#")[2]
            msg += ",name->{},quantity->{},price->{}".format(name, quantity, price)
        print(msg)
        text = ("Thanks {} for shopping with us ,\n\n Your order {} with order id {}, on address {} \n\n your total is "
                "{}").format(
            "dhruv", msg, order_id, order_address, order_total)
        return text


mail = mail()


class RegisterView(MailView):

    def get(self, request):
        return render(request, 'login/register.html')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']

        if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
            context = {"error": "this email or username is already taken try another one"}
            return render(request, 'login/register.html', {"context": context})
        else:
            otp = self.OtpGeneration()
            OTP_email_json = email_content.email_content
            OTP_email_json_subject = OTP_email_json["OTP_Send"]["subject"]
            OTP_email_json_body1 = OTP_email_json["OTP_Send"]["body1"]
            OTP_email_json_body2 = OTP_email_json["OTP_Send"]["body2"]
            message = OTP_email_json_body1 + f"\nYour OTP: {otp}\n" + OTP_email_json_body2
            self.send_email(OTP_email_json_subject, message, email)

            # Store the OTP and timestamp in the session
            request.session['username'] = username
            request.session['password'] = password
            request.session['email'] = email
            request.session['otp'] = otp
            request.session['otp_timestamp'] = str(timezone.now())

            return redirect('/register_verified/')


class LoginView(View):

    def get(self, request):
        return render(request, 'login/login.html')

    def post(self, request, *args, **kwargs):
        email = request.POST['email_address']
        password = request.POST['password']
        print(password)
        try:
            username = User.objects.get(email=email)
            print("email--", email, "password--", username.password, "username--", username.email)
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                print("user logged in")
                return redirect('/')
            else:
                print("user is none")
                context = {'error': 'email and password does not match.'}
                return render(request, 'login/login.html', {'context': context})
        except:
            context = {'error': 'user not found go to register'}
            return render(request, 'login/register.html', {'context': context})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


class ResetView(MailView):

    def get(self, request, *args, **kwargs):
        if request.session.get('otp_verified'):
            print(request.session.get('otp_verified'), "hooooooooooooooooooooooooooo")
            print("yeeeeessss it's verified")
            return render(request, "forget/reset_password.html")
        else:
            print("you need verify via otp first")
            context = "you need verify via otp first"
            return render(request, 'forget/forget.html', {'context': context})

    def post(self, request, *args, **kwargs):
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.session.get("reset_email")
        print(email, password)
        if password == confirm_password:
            try:
                user = User.objects.get(email=email)
                print(user.password)
                user.set_password(password)
                user.save()
                print(user.password)
                success_reset_passwd_email_json = email_content.email_content
                success_reset_passwd_email_json_subject = success_reset_passwd_email_json["successfullyResetPassword"][
                    "subject"]
                success_reset_passwd_email_json_body = success_reset_passwd_email_json["successfullyResetPassword"][
                    "body"]
                message = f"\nDear {user},\n\n" + success_reset_passwd_email_json_body
                self.send_email(success_reset_passwd_email_json_subject, message, email)
                return redirect('/login/')
            except Exception as e:
                print(e, "ee")
                if "User matching query does not exist" in str(e):
                    context = "Email Not Found, Please Register First."
                    return render(request, 'forget/reset_password.html', {'context': context})
                else:
                    context = "Please Try Again !!"
                    return render(request, 'forget/reset_password.html', {'context': context})
        else:
            context = "enter same password"
            return render(request, 'forget/reset_password.html', {'context': context})


class reset_verified(MailView):

    def get(self, request, *args, **kwargs):
        return render(request, 'login/verification.html')

    def post(self, request, *args, **kwargs):
        reset_email = request.session.get("reset_email")
        user_otp = request.POST['otp']
        site = self.Verification(request, reset_email, user_otp)
        request.session['otp_verified'] = True
        if site:
            print("reset_password")
            return redirect('/reset_password/')
        else:
            print("reset_password fail")
        site = '/reset_verified/'
        return render(request, 'login/verification.html', {'site': site})


class VerifyOTPView(MailView):

    def get(self, request):
        return render(request, 'login/verification.html')

    def post(self, request):
        user_otp = request.POST.get('otp')
        a = request.session.get('otp')
        print("my otp", type(user_otp), type(a))
        otp_timestamp_str = request.session.get('otp_timestamp')

        if otp_timestamp_str:
            otp_timestamp = datetime.datetime.strptime(otp_timestamp_str, "%Y-%m-%d %H:%M:%S.%f%z")

            # Check if the OTP has expired (more than 30 seconds old)
            if timezone.now() > otp_timestamp + timedelta(seconds=30):
                context = {"error": "The OTP has expired. Please try again."}
                return render(request, 'login/register.html', {"context": context})

            # Check if the entered OTP matches the one in the session
            if int(user_otp) == int(request.session.get('otp')):
                username = request.session.get('username')
                password = request.session.get('password')
                email = request.session.get('email')

                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                Register_email_content = email_content.email_content
                Register_email_content_subject = Register_email_content["Register"]["subject"]
                Register_email_content_body = Register_email_content["Register"]["body"]
                message = f"""Dear {username},
                 {Register_email_content_body}
                """
                self.send_email(Register_email_content_subject, message, email)

                return redirect("/login/")

        context = "Invalid OTP. Please try again."
        return render(request, 'login/verification.html', {"context": context})


class forget_password(MailView):

    def get(self, request, *args, **kwargs):
        return render(request, 'forget/forget.html')

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        try:
            user = user_email.objects.filter(email=email)
            print(user, "user")
            if user:
                otp = self.OtpGeneration()
                OTP_email_json = email_content.email_content
                OTP_email_json_subject = OTP_email_json["ResetPassword"]["subject"]
                OTP_email_json_body1 = OTP_email_json["ResetPassword"]["body1"]
                OTP_email_json_body2 = OTP_email_json["ResetPassword"]["body2"]
                message = OTP_email_json_body1 + f"\nYour One-Time Password (OTP) for resetting your password is: {otp}. Please use this OTP to proceed with resetting your password.\n\n" + OTP_email_json_body2
                self.send_email(OTP_email_json_subject, message, email)

                request.session['otp'] = otp
                request.session['otp_timestamp'] = str(timezone.now())
                request.session["reset_email"] = email

                request.session["reset_email"] = email
                return redirect('/reset_verified/')
        except Exception as e:
            print(e, "reset e")
            if "user_email matching query does not exist" in str(e):
                context = "Your Email Dose Not Exist, Please Register First."
                return render(request, 'forget/forget.html', {"messages": context})

        return render(request, 'forget/forget.html')


class forget_username(MailView):

    def get(self, request, *args, **kwargs):
        return render(request, 'forget/forget_username.html')

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        try:
            user_username = (User.objects.get(email=email)).username
            print("username", user_username)
            username_email_json = email_content.email_content
            username_email_json_subject = username_email_json["RetriveUsername"]["subject"]
            username_email_json_body1 = username_email_json["RetriveUsername"]["body1"]
            username_email_json_body2 = username_email_json["RetriveUsername"]["body2"]
            message = username_email_json_body1 + f"\n\nYour username for your account is: {user_username}\n\n" + username_email_json_body2
            self.send_email(username_email_json_subject, message, email)
            self.send_email(username_email_json_subject, message, email)
            context = "Your Username Will Send Via Your Mail Please Check It."
            return render(request, 'forget/forget_username.html', {'messages': context})
        except:
            context = "Your Email Dose Not Exits !!"
            return render(request, 'forget/forget_username.html', {'messages': context})


class ProfileView(View):

    def get(self, request, *args, **kwargs):
        try:
            print(request.user.email,"request email ")
            email = request.user.email
            userData = user_address.objects.get(email=email)
            print(type(userData), "data")
            userData.username = request.user
            return render(request, "user_data/user_data.html", {"userData": userData})
        except Exception as e:
            print(e)
        return render(request, "user_data/user_data.html")


class EditProfileView(View):

    def get(self, request, *args, **kwargs):
        return render(request, "user_data/edit_user_data.html")

    def post(self, request, *args, **kwargs):
        firstname = request.POST["FirstName"]
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        building = request.POST['building']
        street = request.POST['street']
        area = request.POST['area']
        pincode = request.POST['pincode']
        city = request.POST['city']
        state = request.POST['state']
        print(firstname, email, phone_number, building, street, area, pincode, city, state)
        user_address.objects.filter(account_email=request.user.email).update(email=email, building=building,
                                                                             street=street, area=area, pincode=pincode,
                                                                             city=city, state=state,
                                                                             phone_number=phone_number)
        
        return redirect("/profile/")


class CashOnDelivery(MailView):
    otp = None

    def get(self, request, *args, **kwargs):
        self.otp = self.OtpGeneration()
        return render(request, "order.html")


class SuccessPlacedOrder(CashOnDelivery):

    def post(self, request, *args, **kwargs):
        print(self.otp)
        user_otp = request.POST.get("otp")
        print(user_otp, "otps")
        if self.otp == user_otp:
            print("success full")
        return render(request, "sucess_order.html")


class shipment:

    def take_user_data(email):
        # take billing data ffrom user_address table and order data table
        print("taking user data",formatted_datetime)
        # user = user_address.objects.get(email=email)
        # user_billing_city = user.city
        # user_billing_pincode = user.pincode
        # user_billing_state = user.state
        # user_billing_email = email
        # user_billing_phone = user.phone_number
        user_billing_city = "ahmedabad"
        user_billing_pincode = "380060"
        user_billing_state = "gujrat"
        user_billing_email = email
        user_billing_phone = "9033474857"
        
        print("user data taked")
        print(user_billing_city,user_billing_phone,user_billing_pincode)
        # take cart data
        order_user = cart_data.objects.get(email=email)
        print(order_user)
        order_address = order_user.address_1
        order_total = order_user.order_total
        print(order_user.products_detail)
        # order_product = ast.literal_eval(order_user.products_detail)
        order_product = order_user.products_detail
        user_name = User.objects.get(email=email).username
        print("products", order_product)

        # add value to final order list
        b = final_order(email=email, address=order_address, products_detail=order_product,
                        order_total=order_total,
                        shiprocket_dashboard=False)
        final_order.save(b)
        print('a1a1')
        order_id = final_order.objects.aggregate(Max('order_id'))['order_id__max']
        # order_id =  final_order.objects.get(email=email AND adress=order_address)

        print("order_id", type(order_id), order_id)

        l2 = []
        # add products  
        print("order_product", order_product, type(order_product))
        for i in order_product:
            print("0000", i,type(i))
            j = json.loads(i)
            p_id= j["product_id"]
            price = j["price"]
            size = j["size"]
            quantity = j["quantity"]
            name =  Product_Details.objects.get(id=p_id).name
            # name = i.split('#')[0]
            # price = i.split('#')[1]
            # size = i.split('#')[2]
            # quantity = i.split('#')[3]
            print("name and quantity", name, quantity, price, size)
            d1 = {
                "name": name,
                "sku": str(name)+"-"+str(size)+"-"+str(price),
                "units": quantity,
                "selling_price": price,
                "discount": "00",
                "tax": "00",
                "hsn": ""
            }
            l2.append(d1)

        order_data = {
            "order_id": 82,
            "shipping_is_billing": True,
            "order_date": "{}".format(formatted_datetime),
            "pickup_location": "Home",
            "channel_id": "",
            "comment": "",
            "reseller_name": "dhruvil",
            "company_name": "",
            "billing_customer_name": user_name,
            "billing_last_name": "",
            "billing_address": order_address,
            "billing_address_2": order_address,
            "billing_isd_code": "",
            "billing_city": user_billing_city,
            "billing_pincode": user_billing_pincode,
            "billing_state": user_billing_state,
            "billing_country": "INDIA",
            "billing_email": user_billing_email,
            "billing_phone": user_billing_phone,
            "billing_alternate_phone": "",
            "shipping_customer_name": "",
            "shipping_last_name": "",
            "shipping_address": "",
            "shipping_address_2": "",
            "shipping_city": "",
            "shipping_pincode": "",
            "shipping_country": "",
            "shipping_state": "",
            "shipping_email": "",
            "shipping_phone": "",
            "order_items": l2,
            "payment_method": "COD",
            "shipping_charges": "0",
            "giftwrap_charges": "0",
            "transaction_charges": "0",
            "total_discount": "0",
            "sub_total": int(order_total)-int((order_total/100)*5),
            "length": "30",
            "breadth": "30",
            "height": "7",
            "weight": "{}".format(int(quantity)*0.4),
            "ewaybill_no": "",
            "customer_gstin": "",
            "invoice_number": "",
            "order_type": ""
        }
        # {'order_id': 430681272, 'shipment_id': 428856942, 'status': 'NEW', 'status_code': 1, 'onboarding_completed_now': 0, 'awb_code': '', 'courier_company_id': '', 'courier_name': ''}
        return order_data

    def shiprocket_key():
        url = "https://apiv2.shiprocket.in/v1/external/auth/login"
        headers = {
            "Content-Type": "application/json"}
        response = requests.post(url, json={
            "email": "dhruv.180670107033@gmail.com",
            "password": "ShipDhruvRocket@1"}, headers=headers)
        a = response.json()
        return a['token']

    def shiprockeet_order_function(request):
        url = "https://apiv2.shiprocket.in/v1/external/orders/create/adhoc"

        # Your API key
        api_key = shipment.shiprocket_key()
        # Headers for the request
        headers = {
            "Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        print('aa')
        order_data = shipment.take_user_data(email=request.user.email)
        print(order_data)
        # Send the POST request
        response = requests.post(url, json=order_data, headers=headers)

        # Print the response
        print(response.status_code)
        print(response.json())
        return redirect('/')
    
    def cancel_order(request):
        ids = request.POST["order_id"]
        print((ids))
        url = "https://apiv2.shiprocket.in/v1/external/orders/cancel"
        # Your API key
        api_key = shipment.shiprocket_key()
        print(api_key,"apikey")
        # Headers for the request
        # ids= 430676810
        headers = {
            "Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        print('aa')
        data = {
                "ids": [ids]
        }
        response = requests.get(url, json=data, headers=headers)
        print(response.status_code)
        return redirect('/')


    def get_order(request,id):
        print(request)
        url = 'https://apiv2.shiprocket.in/v1/external/orders/show/{}'.format(id)

        api_key = shipment.shiprocket_key()
        print(api_key,"apikey","getettttdadadadtataa")
        # Headers for the request
        # ids= 430676810
        headers = {
            "Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        print('aa')
        response = requests.get(url,headers=headers)
        return response
    
    def return_order(request):
        order_id = request.POST('order_id')
        sku = request.POST('sku')
        units = request.POST('units')
        print(order_id,sku,units)

        url = "https://apiv2.shiprocket.in/v1/external/orders/create/return"
        get_data = shipment.get_order(request=request,id=430681272)
        print(get_data,type(get_data))

        user_data = get_data.json()
        print(user_data,type(user_data),"user_datatatatatat")

        api_key = shipment.shiprocket_key()
        print(api_key,"apikey")
        headers = {
            "Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        print('aa')
        
        l2 = []
        # add products  
        # d1 = {
        #     "name": name,
        #     "sku": str(name)+"-"+str(size)+"-"+str(price),
        #     "units": quantity,
        #     "selling_price": price,
        #     "discount": "00",
        #     "tax": "00",
        #     "hsn": ""
        # }
        # l2.append(d1)

        data = {
            "order_id": id,
            "order_date": "2021-12-30",
            "channel_id": user_data["data"]["channel_id"],
            "pickup_customer_name": ["customer_name"],
            "pickup_last_name": "",
            "company_name":"",
            "pickup_address": ["customer_address"],
            "pickup_address_2": "",
            "pickup_city": ["customer_city"],
            "pickup_state": ["customer_state"],
            "pickup_country": "India",
            "pickup_pincode": ["customer_pincode"],
            "pickup_email": ["customer_email"],
            "pickup_phone": ["customer_phone"],
            "pickup_isd_code": "91",
            "shipping_customer_name": "pyrenean clothing",
            "shipping_last_name": "pyrenean clothing",
            "shipping_address": ["pickup_location"],
            "shipping_address_2": "",
            "shipping_city": "ahmedabad",
            "shipping_country": "India",
            "shipping_pincode": 380060,
            "shipping_state": "GUJARAT",
            "shipping_email": "pyrenean@gmail.com",
            "shipping_isd_code": "91",
            "shipping_phone": 9033474857,
            "order_items": [
                {
                "sku": "shirt-M-2709",
                "name": "shoes",
                "units": 1,
                "selling_price": user_data["data"]["products"]["price"],
                "discount": 0,
                "qc_enable":True,
                "hsn": "",
                "brand":"",
                "qc_size":""
                }
                ],
            "payment_method": "COD",
            "total_discount": "0",
            "sub_total": 400,
            "length": 30,
            "breadth": 30,
            "height": 7,
            "weight": user_data["data"]["products"]["quantity"]*units
            }

        response = request.post(url,json=data,headers=headers)
        print(response.json())
        print(response.status_code)
        return redirect('/')

class razor_payment:
    RAZOR_KEY_ID = "rzp_test_PxvxU8NuPVYlN2"
    RAZOR_KEY_SECRET = "KP3FhK8rzOJu5Blo3ZvJHBpj"
    # authorize razorpay client with API Keys.
    razorpay_client = razorpay.Client(auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))

    def check_user_data(request, email):
        try:
            c = user_address.objects.get(email=email)
            print(c, "data is there")
            return True
        except:
            context = "you have to add your address first"
            return False
            # messages.success(request, context)
            # print("you have to add ypur data first")
            # request.session['edit_redirect'] = after_edit
            # return redirect('/edit_user_data/', {"context": context})

        # try:
        #     try:
        #         email = email
        #         order_product_data = []
        #         for i in products_list:
        #             products_detail = str(str(i.name) + "#" + str(i.price))
        #             order_product_data.append(products_detail)
        #         try:
        #             c = user_address.objects.get(email=email)
        #             address = str(c.building) + " , " + str(c.street) + " , " + str(c.area) + " , " + str(
        #                 c.pincode) + " , " + str(c.city) + " , " + str(c.state)

        #             if cart_data.objects.filter(email=email).exists():
        #                 if order_product_data != "":
        #                     user = cart_data.objects.get(email=email)
        #                     user.products_detail = order_product_data
        #                     user.order_total = product_total
        #                     user.address_1 = address
        #                     user.save()
        #                     return render(request, 'cart_checkout/Cart.html',
        #                                   {'products': products_list, 'product_total': product_total})
        #                 else:
        #                     pass
        #             else:
        #                 if order_product_data != "":
        #                     b = cart_data(email=email, address_1=address, products_detail=order_product_data,
        #                                   order_total=product_total)
        #                     cart_data.save(b)
        #                     return render(request, 'cart_checkout/Cart.html',
        #                                   {'products': products_list, 'product_total': product_total})
        #                 else:
        #                     pass
        #         except:
        #             context = "you have to add your address first"
        #             messages.success(request, context)
        #             after_edit = f"ProductDetails/{slug}"
        #             request.session['edit_redirect'] = after_edit
        #             return redirect('/edit_user_data/', {"context": context})
        #     except:
        #         context = "you have't login yet"
        #         messages.success(request, context)
        #         return redirect('/login/', {"context": context})
        # except:
        #     product_total = 0
        #     products_list = []
        #     return render(request, 'cart_checkout/cart.html',
        #                   {'products': products_list, 'product_total': product_total})

    def homepage(self, request, razorpay_client=razorpay_client, RAZOR_KEY_ID=RAZOR_KEY_ID):
        email = request.user.email
        check_data = razor_payment.check_user_data(request=request, email=email)
        print("razor front page")
        if check_data:
            order_user = cart_data.objects.get(email=email)
            print("razor front page ")
            order_address = order_user.address_1
            print(order_user)
            order_total = order_user.order_total
            order_product = order_user.products_detail

            print(order_user, order_address, order_total, order_product, "initial")

            currency = 'INR'
            amount = order_total * 100  # Rs. 200

            # Create a Razorpay Order
            razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                               currency=currency,
                                                               payment_capture='0'))

            # order id of newly created order.
            razorpay_order_id = razorpay_order['id']
            callback_url = 'paymenthandler/'

            # we need to pass these details to frontend.
            context = {}
            context['razorpay_order_id'] = razorpay_order_id
            context['razorpay_merchant_key'] = RAZOR_KEY_ID
            context['razorpay_amount'] = amount
            context['currency'] = currency
            context['callback_url'] = callback_url
            # c = user_address.objects.get(email=email)
            # address = str(c.building) +" , "+ str(c.street) + " , " + str(c.area) +" , "+ str(c.pincode) +" , "+ str(c.city)
            # print(address)
            context['address'] = order_address
            context["order_total"] = order_total
            msg = ""
            for i in order_product:
                print(i, len(i), "hiiiiiiiiiiiiiiiiii")
                i = json.loads(i)
                name = i["product_id"]
                quantity = i["quantity"]
                price = i["price"]
                msg += "\n{}-{}-{}".format(name, quantity, price)
            context["order_product"] = msg
            return render(request, 'cart_checkout/razor_front.html', context=context)
        else:
            print("you have to add your address first")
            context = "you have to add your address first"
            messages.success(request, context)
            request.session['edit_redirect'] = 'initiate_payment'
            return redirect('/EditProfile/', {"context": context})

    @csrf_exempt
    def paymenthandler(self, request, razorpay_client=razorpay_client):
        print("after payment", request.method)
        # only accept POST request.

        if request.method == "POST":
            try:
                # get the required parameters from post request.
                payment_id = request.POST.get('razorpay_payment_id', '')
                razorpay_order_id = request.POST.get('razorpay_order_id', '')
                signature = request.POST.get('razorpay_signature', '')
                params_dict = {
                    'razorpay_order_id': razorpay_order_id,
                    'razorpay_payment_id': payment_id,
                    'razorpay_signature': signature
                }
                print("1111111")
                # verify the payment signature.
                result = razorpay_client.utility.verify_payment_signature(
                    params_dict)
                print(result, "result")
                if result is not None:
                    # email = "ladoladhruv5218@gmail.com"
                    email = request.user.email
                    print(email)
                    order_user = cart_data.objects.get(email=email)
                    print("order_user")
                    order_total = order_user.order_total
                    print(order_total)
                    amount = order_total * 100  # Rs. 200
                    try:
                        print("22222222")
                        # capture the payemt
                        razorpay_client.payment.capture(payment_id, amount)
                        print("payment captured")
                        # render success page on successful caputre of payment
                        a = shipment.shiprockeet_order_function(request)
                        print(a, "aa")

                        print(a.status_code)
                        if a.status_code == 200 and a.json()['status'] == "NEW":
                            print("readyyyyy")
                            order_id = final_order.objects.aggregate(Max('order_id'))['order_id__max']
                            order = final_order.objects.get(order_id=order_id)
                            order.shiprocket_dashboard = True
                            order.save()

                            text = mail.confirm_order_mail(email="ladoladhruv5218@gmail.com")
                            text
                            print(text)
                            mail.send_mail(email="ladoladhruv5218@gmail.com", msg=text)

                            print("shipment done")
                            try:
                                order_user = cart_data.objects.get(email="ladoladhruv5218@gmail.com")
                                order_user.delete()
                            except:
                                print(KeyError)

                            print("cart empty")
                            print("cart data is deleted")
                            return redirect('/')
                        else:
                            pass
                        print(a.status_code)
                        print(a.json()['status'])
                        print("ship rocket api is succefully done")
                        return render(request, 'cart_checkout/paymentsuccess.html')
                    except:
                        print("4444444")
                        # if there is an error while capturing payment.
                        return render(request, 'cart_checkout/paymentfail.html')
                else:

                    # if signature verification fails.
                    return render(request, 'cart_checkout/paymentfail.html')
            except:

                # if we don't find the required parameters in POST data
                print("error")
                return HttpResponseBadRequest()
        else:
            print("method not allowed")
            # if other than POST request is made.
            return HttpResponseBadRequest()

    def cashfree(self, email):
        # prepeare data
        # order_id = final_order.objects.aggregate(Max('order_id'))['order_id__max']
        # linkid = "00"+"{}".format(order_id)
        # order = final_order.objects.get(order_id=order_id)
        # order.link_id = linkid
        # order.save()
        order_id = 1000
        # order_user = cart_data.objects.get(email=email)
        # order_total = order_user.order_total
        # amount = order_total * 100  # Rs. 200
        amount = 100
        # name = User.objects.get(email=email).username
        # number = user_address.objects.get(email=email).phone_number
        name = "dhruv"
        number = 9033474857

        url = "https://sandbox.cashfree.com/pg/links"

        payload = {
            "customer_details": {
                "customer_phone": "{}".format(number),
                "customer_email": email,
                "customer_name": "{}".format(name)
            },

            "link_notify": {
                "send_sms": True,
                "send_email": True
            },
            "link_meta": {"return_url": "http://127.0.0.1:8000/cashfree_handle"},
            "link_id": "{}".format("00" + "{}".format(order_id)),
            "link_amount": amount,
            "link_currency": "INR",
            "link_purpose": "Payment for PlayStation 11",
            # "link_expiry_time": "2021-10-14T15:04:05+05:30"
        }
        headers = {
            "accept": "application/json",
            "x-api-version": "2022-09-01",
            "content-type": "application/json",
            "x-client-id": "TEST10048875274ada62a720a9b6c35757884001",
            "x-client-secret": "TEST820409eead5db1fa07b95f96212cb4f2a0650a8"
        }

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return response

    def cashfree_dashboard(self, request):
        print(request.user.email)
        dashboard = self.cashfree(email=request.user.email)
        data = dashboard.text
        print(type(data))
        data_a = json.loads(data)
        link = data_a["link_url"]
        return redirect(link)

    def cashfree_handle(self, request):
        print(request)

        # order_id = final_order.objects.aggregate(Max('order_id'))['order_id__max']
        # order = final_order.objects.get(order_id=order_id)
        # linkid = order.link_id
        # ship_Status = order.shiprocket_dashboard
        # email = order.email
        email = request.user.email

        print(request)
        linkid = "1000"
        url = "https://sandbox.cashfree.com/pg/links/{}".format(linkid)
        print(url)

        headers = {
            "accept": "application/json",
            "x-api-version": "2022-09-01",
            "x-client-id": "TEST10048875274ada62a720a9b6c35757884001",
            "x-client-secret": "TEST820409eead5db1fa07b95f96212cb4f2a0650a8"
        }

        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        payment_status = data["link_status"]

        if payment_status == "PAID":
            if ship_status == False:
                # a = shipment.shiprockeet_order_function(request,email=email)
                # print(a.status_code)

                # if a.status_code == 200 and a.json()['status'] == "NEW":
                #     print("readyyyyy")
                #     order_id = final_order.objects.aggregate(Max('order_id'))['order_id__max']
                #     order = final_order.objects.get(order_id=order_id)
                #     order.shiprocket_dashboard = True
                #     order.save()

                #     text = mail.confirm_order_mail(email="ladoladhruv5218@gmail.com")
                #     text

                #     mail.send_mail(email="ladoladhruv5218@gmail.com", msg=text)

                #     print("shipment done")
                #     try:
                #         order_user = cart_data.objects.get(email="ladoladhruv5218@gmail.com")
                #         order_user.delete()
                #     except:
                #         print(KeyError)

                #     print("cart empty")
                #     print("cart data is deleted")
                #     print(a.status_code)
                #     print(a.json()['status'])
                #     print("ship rocket api is succefully done")
                return render(request, 'cart_checkout/paymentsuccess.html')
                # else:
                # pass
                # return render(request, 'cart_checkout/paymentfail.html')

            else:
                return render(request, 'cart_checkout/paymentsuccess.html')
        else:
            return HttpResponseBadRequest("payment fail")
        # return redirect('/')

    def Cash_on_delivery(request):
        email = request.user.email
        # ship_status = cart_data.object.get()
        
        # if ship_Status == False:
        a = shipment.shiprockeet_order_function(request,email=email)
        print(a.status_code)

        if a.status_code == 200 and a.json()['status'] == "NEW":
            print("readyyyyy")
            order_id = final_order.objects.aggregate(Max('order_id'))['order_id__max']
            order = final_order.objects.get(order_id=order_id)
            ship_Status = order.shiprocket_dashboard
            print("order id is",order_id)
            print("order is",order)
            print("ship status is",ship_Status)
    
            order.shiprocket_dashboard = True            
            order.save()

            # text = mail.confirm_order_mail(email="ladoladhruv5218@gmail.com")
            # text

            # mail.send_mail(email="ladoladhruv5218@gmail.com", msg=text)

            print("shipment done")
            try:
                order_user = cart_data.objects.get(email=email)
                order_user.delete()
            except:
                print(KeyError)

            print("cart empty")
            print("cart data is deleted")
            print(a.status_code)
            print(a.json()['status'])
            print("ship rocket api is succefully done")
            return render(request, 'cart_checkout/paymentsuccess.html')

        else:
                print("some issue  in ship rocket")
                return HttpResponseBadRequest("there is some issue with our delivery agent we will reach put to  you soon")

                # return render(request, 'cart_checkout/paymentfail.html')
        # else:
        #     return render(request, 'cart_checkout/paymentsuccess.html')
        

Rozor = razor_payment()

# prevent_refresh_middleware.py

from django.http import HttpResponseRedirect

class PreventRefreshMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/COD/':
            # Prevent refreshing for the specific page
            return HttpResponseRedirect('/')  # Redirect to the home page

        response = self.get_response(request)
        return response
