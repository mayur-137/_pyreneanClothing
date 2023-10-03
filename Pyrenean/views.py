from django.views.generic.base import TemplateView
from django.http import HttpResponse, Http404
from django.views.generic.edit import CreateView
from .models import Mens, Women, UniSex, ContactModel, user_data, CartModel, Size,user_email
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactFormModel
from django.contrib.auth.models import User, auth
from django.views import View
from django.contrib import messages
import random ,smtplib

global product_total, getSize_id, getSize, slug


class HomeView(TemplateView):
    template_name = "Home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["Mens"] = Mens.objects.all()
        context["Kids"] = UniSex.objects.all()
        context["Women"] = Women.objects.all()
        for cnt in context:
            if cnt == "view":
                continue
            for data in context[cnt]:
                data.discounted_price = int(data.price - (data.price * data.discount / 100)) + 1

        context['Size'] = Size.objects.all()

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
    template_name = "Product-Details.html"

    def get_context_data(self, **kwargs):
        global slug, getSize, getSize_id
        VG = super().get_context_data()
        slug = self.kwargs.get("slug")
        getSize = self.kwargs.get("size")
        getSize_id = self.kwargs.get("id")
        if getSize is not None and getSize_id is not None:
            getSize = getSize.split("=")[1]
            getSize_id = getSize_id.split("=")[1]
            print(getSize, getSize_id, slug, "firstcheck")
        VG["PRD"] = Mens.objects.filter(slug=slug)
        if not VG["PRD"]:
            VG["PRD"] = UniSex.objects.filter(slug=slug)
        if not VG["PRD"]:
            VG["PRD"] = Women.objects.filter(slug=slug)
        print(VG['PRD'], "PRD")
        for data in VG['PRD']:
            data.discounted_price = int(data.price - (data.price * data.discount / 100)) + 1
            print(data.discounted_price)

        VG['Size'] = Size.objects.all()
        max_quantity = 0
        max_size = None
        for size in VG['Size']:
            if (size.men_id == data.id or size.kid_id == data.id or size.women_id == data.id) and size.quantity > max_quantity:
                data.max_quantity = size.quantity
                data.max_size = size.size
        return VG


class CustomerServiceView(TemplateView):
    template_name = "Customer-Service.html"

    def get_context_data(self, **kwargs):
        customerService = super().get_context_data()
        return customerService


class AddToCartView(View):

    def post(self, request, *args, **kwargs):
        print("addd-----------too-----------cart")
        product_id = request.POST.get('product_id')
        current_user = request.user
        email = current_user.email
        print(email, "email")
        product = Size.objects.filter(men_id=product_id)
        if not product:
            product = Size.objects.filter(kid_id=product_id)
        if not product:
            product = Size.objects.filter(women_id=product_id)
        print(product, "product",product_id)
        
        checkCart = CartModel.objects.filter(product_id=product_id)
        print(checkCart, "checkCart")
        
        if not checkCart:
            print("checkcart")
            addCart = CartModel(product_id=product_id, email=email).save()
        for detail in product:
            print(detail.quantity, "quantity11111111", detail.id, product_id)
        
        cart_session = request.session.get('cart_session', {})
        print(cart_session, "11")
        
        if cart_session.get(product_id) is None or cart_session.get(product_id) < detail.quantity:
            print("hey")
            cart_session[product_id] = cart_session.get(product_id, 0) + 1
            request.session['cart_session'] = cart_session
        # if cart_session.get(product_id) == detail.quantity:
        #     details.stock = False
        #     for model in models:
        #         try:
        #             updateStock = model.objects.filter(id=product_id).update(stock=details.stock)
        #         except:
        #             pass
        return redirect("/cart/")


class CartView(View):
    model = CartModel

    def get(self, request, *args, **kwargs):
        print("cartt------------vieww")
        # global product
        products_in_cart = []
        products_list = []
        # products_list.clear()
        product_total = 0
        cart = request.session.get('cart_session', {})
        print(cart, "3")
        models = [Mens, UniSex, Women]
        for model in models:
            try:
                itm = model.objects.filter(id__in=cart.keys())
                if itm:
                    products_in_cart.append(itm)
            except:
                pass
        print(products_in_cart,"products in cart")
        for products in products_in_cart:
            for product in products:
                product.subtotal = product.price * cart[str(product.id)]
                product_total = product.subtotal + product_total
                product.product_quantity = str(cart[str(product.id)])
                print(getSize, product.id, "checking")
                if getSize is None and slug is None:
                    messages.error(request, "Please select a size first")
                    return redirect(f"/ProductDetails/{slug}")
                else:
                    product.size = getSize
                    checkCart = Size.objects.filter(size=getSize)
                    print(checkCart, "checkCart11")
                for mysize in checkCart:
                    pass
                
                print(mysize.id,getSize_id,"compare")
                print(mysize.size,getSize,"compare")

                if str(mysize.size) == str(getSize):
                    print(mysize.size, getSize_id,"myid")
                    print(product.id,"product----------id")
                    updateCart = CartModel.objects.filter(product_id=product.id).update(size_id=mysize.id, size=mysize.size, quantity=mysize.quantity)
                    print("done")
                    # if checkCart:
                    #     checkSize = Size.objects.filter(id=getSize_id)
                    #     checkCart.update(size=getSize)
                products_list.append(product)

        return render(request, 'cart.html', {'products': products_list, 'product_total': product_total})


class Update_cart_view(View):

    def post(self, request, *args, **kwargs):
        Product_id = request.POST.get("Update_product_quantity")
        print(Product_id, "ID")
        Mode_of_Operations = request.POST.get("minus")
        # models = [Mens, Kid, Women]
        # for model in models:
        #     try:
        #         product = model.objects.filter(id=Product_id)
        #         for details in product:
        #             for detail in details.size.all():
        #                 pass
        #     except:
        #         pass
        product = Size.objects.filter(men_id=Product_id)
        if not product:
            product = Size.objects.filter(kid_id=Product_id)
        if not product:
            product = Size.objects.filter(women_id=Product_id)
        print(product)
        for detail in product:
            print(detail.quantity)
        if Mode_of_Operations == "-":
            cart_session = request.session.get('cart_session', {})
            cart_session[Product_id] = cart_session.get(Product_id) - 1
            request.session['cart_session'] = cart_session
            # if cart_session.get(Product_id) < detail.quantity:
            #     details.stock = True
            #     for model in models:
            #         try:
            #             updateStock = model.objects.filter(id=Product_id).update(stock=details.stock)
            #         except:
            #             pass
            if cart_session.get(Product_id) == 0:
                del cart_session[Product_id]
        else:
            cart_session = request.session.get('cart_session', {})
            if not cart_session.get(Product_id) == detail.quantity:
                cart_session[Product_id] = cart_session.get(Product_id) + 1
                request.session['cart_session'] = cart_session
            else:
                pass
                # details.stock = False
                # for model in models:
                #     try:
                #         updateStock = model.objects.filter(id=Product_id).update(stock=details.stock)
                #     except:
                #         pass
        return redirect("/cart/")


class RemoveItemView(View):

    def post(self, request, *args, **kwargs):
        GetRemoveItemId = request.POST.get("removeItem")
        cart_session = request.session.get('cart_session', {})
        models = [Mens, UniSex, Women]
        for model in models:
            try:
                product = model.objects.filter(id=GetRemoveItemId)
                for details in product:
                    pass
            except:
                pass
        if not details.stock:
            details.stock = True
            for model in models:
                try:
                    updateStock = model.objects.filter(id=GetRemoveItemId).update(stock=details.stock)
                except:
                    pass
        if GetRemoveItemId in cart_session:
            del cart_session[GetRemoveItemId]
            request.session['cart_session'] = cart_session
        return redirect("/cart/")


class LoginView(TemplateView):
    template_name = "login/login.html"


class mail_otp():
    def otp_generation():
        print("generate otp")
        n = random.randint(1000,9999)
        print(n)
        return n
        
    def send_mail(email,msg):
        server=smtplib.SMTP('smtp.gmail.com',587)
        #adding TLS security 
        server.starttls()
        #get your app password of gmail ----as directed in the video
        email_id = "dhruv.180670107033@gmail.com"
        password='nqdf jevl qqwx guvo'
        server.login(email_id,password)
        #generate OTP using random.randint() function
        # otp=''.join([str(random.randint(0,9)) for i in range(4)])    
        sender='dhruv.180670107033@gmail.com'  #write email id of sender
        receiver=email #write email of receiver
        server.sendmail(sender,receiver,msg)
        print("mail send succefully")
        server.quit()

    def confirm_order_mail(email):
        print('text is generating')
        username = (User.objects.get(email=email)).username
        print("username",username)
        order_id = final_order_list.objects.aggregate(Max('order_id'))['order_id__max']
        order_user = final_order_list.objects.filter(order_id=order_id).first()
        order_total = order_user.order_total
        order_address = order_user.address
        print("order address is ready")
        order_product = ast.literal_eval(order_user.products_detail)
        print("order products are ready to ship",order_product)
        msg = ""
        for i in order_product:
            name = i.split("#")[0]
            quantity = i.split("#")[1]
            price = i.split("#")[2]
            msg += ",name->{},quantity->{},price->{}".format(name,quantity,price)
        print(msg)
        text = "Thanks {} for shopping with us ,\n\n Your order {} with order id {}, on address {} \n\n your total is {}".format(username,msg,order_id,order_address,order_total)
        return text
        
        
    def store_otp(email,otp):
        if user_email.objects.filter(email=email).exists():
                    print("already registred")
                    user = user_email.objects.get(email=email)
                    user.email = email
                    user.otp = otp
                    user.save()
        else:
            print("new user")
            b = user_email(email=email,otp=otp)
            user_email.save(b)

    def verification(email,user_otp):
            print(user_otp,email)
            user = user_email.objects.get(email=email)
            otp = user.otp
            
            if int(user_otp) == int(otp):
                print("verified")
                return "yes"
                # return redirect('main:edit_user_data')
            else:
                print("verification failed")
                return "no"
                # return render(request,'main/verification.html')
        # else:
        #     return render(request, 'main/verification.html')
class login_register():
    
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
                return render(request, 'login/register.html', {'context': context})
            elif User.objects.filter(email=email).exists():
                print("this email is already taken try another one")
                context = {"error": "this email is already taken try another one"}
                return render(request, 'login/register.html', {"context": context})
            else:
                user = User.objects.create_user(username=username, password=password, email=email)
                user.save()
                otp = mail_otp.otp_generation()
                mail_otp.send_mail(email=email,msg="welcome{},your otp is {}".format(username,otp))
                mail_otp.store_otp(email=email,otp=otp)
                print("user created")
                # context = {'error': 'User registered successfully!'}
                return redirect('/register_verified/')
        else:
            print("noooo")
            return render(request, 'login/register.html')
        

        # return render (request=request, template_name="main/register.html", context={"register_form":form})


    @csrf_exempt
    def login_request(request):
        if request.method == "POST":
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
                    return redirect('/test/')
                else:
                    print("user is none")
                    context = {'error': 'email and password does not match.'}
                    return render(request, 'login/login.html', {'context': context})
            except:
                context = {'error': 'user not found go to register'}
                return render(request, 'login/login.html', {'context': context})
        else:
            return render(request, 'login/login.html')

    @csrf_exempt
    def logout_request(request):
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect("/")

class reset():
    def reset_passsowrd(request):
        if request.session.get('otp_verified'):
            print(request.session.get('otp_verified'))
            print("yeeeeessss it's verified")
            if request.method == "POST":
                password = request.POST['password']
                confirm_password = request.POST['confirm_password']
                email = request.POST['email']
                print(email,password)
                if password == confirm_password:
                    print("both passsword is natched")
                    try:
                        user = User.objects.get(email=email)
                        print(user.password)
                        user.set_password(password)
                        user.save()
                        print(user.password)
                        print("user data changed")
                        return redirect('/login/')
                    except:
                        print("no not saved")
                else:
                    context = "enter same password"
                    return render(request,'forget/reset_password.html',{'context':context})
            else:
                return render  (request,'forget/reset_password.html')
        else:
            print("you need verify via otp first")
            context = "you need verify via otp first"
            return render(request,'forget/forget.html',{'context':context})
        
    def reset_verified(request):
        if request.method == "POST":
            user_otp = request.POST['otp']
            email = request.POST['email']
            site = mail_otp.verification(email,user_otp)
            request.session['otp_verified'] = True
            if site == "yes":
                return redirect('/reset_password/')
        else:
            site = '/reset_verified/'
            return render(request, 'login/verification.html',{'site':site})

    def register_verified(request):
        if request.method == "POST":
            user_otp = request.POST['otp']
            email = request.POST['email']
            site =mail_otp.verification(email,user_otp)
            if site == "yes":
                request.session['edit_redirect'] = "login"
                return redirect('/edit_user_data/')
            else:
                return render(request, 'login/verification.html',{'context':"otp does't match to email id"})    
        else:
            site = '/register_verified/'
            return render(request, 'login/verification.html',{'site':site})

    def forget_password(request):
        if request.method == "POST":
            email = request.POST['email']
            otp = mail_otp.otp_generation()
            mail_otp.send_mail(email=email,msg="your otp is {}".format(otp))
            mail_otp.store_otp(email,otp)
            return redirect('/reset_verified/')
        else:
            return render(request,'forget/forget.html')

    def forget_username(request):
        if request.method == "POST":
            email = request.POST['email']
            user_username = (User.objects.get(email=email)).username
            print("username",user_username)
            mail_otp.send_mail(email=email,msg="your username is {}".format(user_username))
            return redirect('/login/')
        else:
            return render(request,'forget/forget_username.html')

class user_datas():
    from .models import user_data  # Make sure the import path is correct
    
    def user_data_function(request):
        current_user = request.user
        email = current_user.email
        if email:
            try:
                print("user data already stored ")
                username = (User.objects.get(email=email)).username
                phone_number = user_data.objects.get(email=email).phone_number
                building = user_data.objects.get(email=email).building
                street = (user_data.objects.get(email=email)).street
                area = (user_data.objects.get(email=email)).area
                pincode = (user_data.objects.get(email=email)).pincode
                city = (user_data.objects.get(email=email)).city
                state = (user_data.objects.get(email=email)).state
                context = {"email": email,"phone_number": phone_number, 'username': username, 'building': building,
                        'street': street, 'area': area, 'pincode': pincode, 'city': city, 'state': state}
                print(context)
                request.session['edit_redirect'] = "user_data"
                return render(request, 'user_data/user_data.html', {'context': context})

            except:
                return render(request, 'user_data/user_data.html')
        else:
            return render(request, 'user_data/user_data.html')


    @csrf_exempt
    def edit_user_data(request):
        print("edit user data")
        if request.method == "POST":
            print("edit user data222")
            email = request.POST['email']
            building = request.POST['building']
            street = request.POST['street']
            area = request.POST['area']
            pincode = request.POST['pincode']
            city = request.POST['city']
            state = request.POST['state']
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
                user.state = state
                user.save()
            else:
                print("user data is not saved")
                b = user_data(email=email, building=building, street=street, area=area, pincode=pincode, city=city,
                            phone_number=phone_number, state=state)
                user_data.save(b)
                print("saved new data")
                return redirect('/test/')
            
            edit_change = request.session.get('edit_redirect')
            return redirect('/{}/'.format(edit_change))
        
            # if edit_change == "login":
            #     return redirect('/login/')
            # elif edit_change == "user_data":
            #     return redirect('/user_data/')
            # else:
            #     return redirect('/test/')
            
        else:
            print("GET")
            return render(request, 'user_data/edit_user_data.html')
