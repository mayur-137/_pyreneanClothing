from django.views.generic.base import TemplateView
from django.http import HttpResponse, Http404  ,HttpResponseBadRequest
from django.views.generic.edit import CreateView
from .models import Mens, Women, UniSex, ContactModel, user_data, CartModel, Size,user_email,cart_data,final_order
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from .forms import ContactFormModel
from django.contrib.auth.models import User, auth
from django.views import View
from django.contrib import messages
import random ,smtplib ,requests , ast , razorpay
from django.db.models import Max
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
        for i  in cart:
            product = Mens.objects.get(id=i)
            sizes = product.get_sizes()
            print("sizessssss",sizes)
        for  j in sizes:
            print(j)
        for model in models:
            try:
                itm = model.objects.filter(id__in=cart.keys())
                if itm:
                    products_in_cart.append(itm)
            except:
                pass
        print(products_in_cart,"products in cart")
        #dhruv
        try:
            print(getSize,getSize_id,"checking")
            print("frommm----------product-------page") 

            if getSize is None and getSize_id is None:
                messages.error(request, "Please select a size first")
                return redirect(f"/ProductDetails/{slug}")
            else:
                for products in products_in_cart:
                    for product in products:
                        product.size = getSize
                        print("size",product.id,str(cart[str(product.id)]),product.size)
                        product.subtotal = product.price * cart[str(product.id)]
                        product_total = product.subtotal + product_total
                        product.product_quantity = str(cart[str(product.id)])
                        # print(product,"product")
                        products_list.append(product)

            # print(product.id,getSize_id,"compare")
            # print(product.id,getSize,"compare")

            # if str(mysize.size) == str(getSize):
            #     print(mysize.size, getSize_id,"myid")
            #     print(product.id,"product----------id")
            #     updateCart = CartModel.objects.filter(product_id=product.id).update(size_id=mysize.id, size=mysize.size, quantity=mysize.quantity)
            #     print("done")
            #     if checkCart:
            #         checkSize = Size.objects.filter(id=getSize_id)
            #         checkCart.update(size=getSize)

            try:
                print("products_list",products_list)
                email = "ladoladhruv5218@gmail.com"
                order_product_data = []
            #     email = request.user.email
                # print(email, "email")
                for i in products_list:
                    # print("item",i.name,i.price,i.subtotal,i.product_quantity,getSize)
                    print("size")
                    products_detail = str(str(i.name) + "#" + str(i.price)+"#"+(str(i.size))+"#"+(str(i.product_quantity))+"#"+(str(i.subtotal)))
                    order_product_data.append(products_detail)
                    # order_product_data += str(","+products_detail + "\n")
                print("order_prodyct_data",order_product_data)
                try:
                    email = "ladoladhruv5218@gmail.com"
                    c = user_data.objects.get(email=email)
                    # print(c, "cccccccccc")
                    address = str(c.building) + " , " + str(c.street) + " , " + str(c.area) + " , " + str(c.pincode) + " , " + str(c.city) + " , " + str(c.state)
                    
                    if cart_data.objects.filter(email=email).exists():
                        if order_product_data != "":
                            # print("user data is there")
                            user = cart_data.objects.get(email=email)
                            user.products_detail = (order_product_data)
                            user.order_total = product_total
                            # print(address)
                            user.address_1 = address
                            user.save()
                            # print("user data changged render to cart")                                # products_list = []
                            # product_total = 20030
                            # print(products_list,"product_list")
                            return render(request, 'cart_checkout/Cart.html', {'products': products_list, 'product_total': product_total})

                        else:
                            pass
                    else:
                        if order_product_data != "":
                            # print("user data is not there")
                            b = cart_data(email=email, address_1=address, products_detail=order_product_data,
                                    order_total=product_total)
                            cart_data.save(b)
                            # print("user data saved")
                            # print(products_list,"product_list")
                            return render(request, 'cart_checkout/Cart.html', {'products': products_list, 'product_total': product_total})

                        else:
                            pass
                    # return render(request, 'cart_checkout/Cart.html', {'products': products_list, 'product_total': product_total})
                
                except:
                    context = "you have to add your address first"
                    print("you have to add your address first-------------------------------")
                    messages.success(request,(context))
                    after_edit = (f"ProductDetails/{slug}")
                    print(after_edit,"after edit")
                    request.session['edit_redirect'] = after_edit
                    return redirect('/edit_user_data/',{"context":context})
            except:
                context = "you have't login yet"
                print("you have't login yet-------------------------------------")
                messages.success(request,(context))
                return redirect('/login/',{"context":context})
        except:
            print("not from product page------------------")
            product_total = 0
            products_list = []
            return render(request, 'cart_checkout/cart.html', {'products': products_list, 'product_total': product_total})

        #         context = "you have to add your address first"
        #         print("you have to add your address first")
        #         messages.success(request,(context))
        #         return redirect('/edit_user_data/',{"context":context})
            
        # except:
        #     print("no log in user")
        #     return render(request, 'cart_checkout/Cart.html')
        
        # return render(request, 'cart.html', {'products': products_list, 'product_total': product_total})


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
        # username = (User.objects.get(email="ladoladhruv5218@gmail.com")).username
        # print("username",username)
        order_id = final_order.objects.aggregate(Max('order_id'))['order_id__max']
        print("111111",order_id)
        order_user = final_order.objects.get(order_id=order_id)
        print('22222')
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
        text = "Thanks {} for shopping with us ,\n\n Your order {} with order id {}, on address {} \n\n your total is {}".format("dhruv",msg,order_id,order_address,order_total)
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
        try:
            email  =  "ladoladhruv5218@gmail.com"
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
        except:
            print('no user found')
            return redirect('/login/',{"context":"you have't logged in "})


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
                
                edit_change = request.session.get('edit_redirect')
                print(edit_change,"edit_change")
                # return redirect('/ProductDetails/2')
                return redirect('/{}'.format(edit_change))
        
            else:
                print("user data is not saved")
                b = user_data(email=email, building=building, street=street, area=area, pincode=pincode, city=city,
                            phone_number=phone_number, state=state)
                user_data.save(b)
                return redirect('/')
            
        else:
            print("GET")
            return render(request, 'user_data/edit_user_data.html')


    
@csrf_exempt
def terms_conditions(request):
    if request.method:
        return render(request, 'cont_term/terms_conditions.html')
    else:
        return redirect("/")


"""shipment code """
class shipment():

    def take_user_data(email):
        # take billing data ffrom user_data table and order data table
        print("taking user data")
        user = user_data.objects.get(email="ladoladhruv5218@gmail.com")
        user_billing_city = user.city
        user_billing_pincode = user.pincode
        user_billing_state = user.state
        user_billing_email = email
        user_billing_phone = user.phone_number
        print("user data taked")
        #take cart data
        order_user = cart_data.objects.get(email="ladoladhruv5218@gmail.com")
        print(order_user)
        order_address = order_user.address_1
        order_total = order_user.order_total
        print('11')
        order_product = ast.literal_eval(order_user.products_detail)
        
        print("products", order_product)

        # add value to final order list
        b = final_order(email="ladoladhruv5218@gmail.com", address=order_address, products_detail=order_product, order_total=order_total,
                            shiprocket_dashboard=False)
        final_order.save(b)
        print('a1a1')
        order_id = final_order.objects.aggregate(Max('order_id'))['order_id__max']
        # order_id =  final_order.objects.get(email=email AND adress=order_address)
        
        print("order_id", type(order_id), order_id)

        l2 = []
        # add products  
        print("order_product",order_product,type(order_product))
        for i in order_product:
            print("0000",i)
            name = i.split('#')[0]
            price = i.split('#')[1]
            size = i.split('#')[2]
            quantity = i.split('#')[3]
            print("name and quantity",name,quantity,price,size)
            d1 = {
                "name": name,
                "sku": i,
                "units": quantity,
                "selling_price": price,
                "discount": "00",
                "tax": "00",
                "hsn": ""
            }
            l2.append(d1)

        order_data = {
            "order_id": 45,
            "shipping_is_billing": True,
            "order_date": "2023-08-28 17:17",
            "pickup_location": "Home",
            "channel_id": "",
            "comment": "",
            "reseller_name": "dhruv",
            "company_name": "",
            "billing_customer_name": "dhruv",
            "billing_last_name": "patel",
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
            "payment_method": "prepaid",
            "shipping_charges": "0",
            "giftwrap_charges": "0",
            "transaction_charges": "0",
            "total_discount": "0",
            "sub_total": order_total,
            "length": "10",
            "breadth": "15",
            "height": "20",
            "weight": "1",
            "ewaybill_no": "",
            "customer_gstin": "",
            "invoice_number": "",
            "order_type": ""
        }
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
        order_data = shipment.take_user_data(email="ladoladhruv5218@gmail.com")
        print(order_data)
        # Send the POST request
        response = requests.post(url, json=order_data, headers=headers)

    # Print the response
        print(response.status_code)
        print(response.json())
        return response

"""razor pay code"""
class razor_payment():
    global razorpay_client , RAZOR_KEY_ID , RAZOR_KEY_SECRET 
    RAZOR_KEY_ID = "rzp_test_PxvxU8NuPVYlN2"
    RAZOR_KEY_SECRET = "KP3FhK8rzOJu5Blo3ZvJHBpj"
    # authorize razorpay client with API Keys.
    razorpay_client = razorpay.Client(
        auth=(RAZOR_KEY_ID, RAZOR_KEY_SECRET))


    def homepage(request):
        email = "ladoladhruv5218@gmail.com"
        order_user = cart_data.objects.get(email=email)
        print(order_user)
        order_address = order_user.address_1
        order_total = order_user.order_total
        order_product =ast.literal_eval(order_user.products_detail)

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
        # c = user_data.objects.get(email=email)
        # address = str(c.building) +" , "+ str(c.street) + " , " + str(c.area) +" , "+ str(c.pincode) +" , "+ str(c.city)    
        # print(address)
        context['address'] = order_address
        context["order_total"] = order_total
        msg = ""
        for i in order_product:
            name = i.split("#")[0]
            quantity = i.split("#")[1]
            price = i.split("#")[2]
            msg += "\n{}-{}-{}".format(name,quantity,price)
        context["order_product"] = msg
        return render(request, 'cart_checkout/razor_front.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
    @csrf_exempt
    def paymenthandler(request):
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
                print(result,"result")
                if result is not None:
                    email = "ladoladhruv5218@gmail.com"
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
                        a
                        print(a.status_code)
                        if a.status_code == 200 and a.json()['status'] == "NEW":
                            print("readyyyyy")
                            order_id = final_order.objects.aggregate(Max('order_id'))['order_id__max']
                            order = final_order.objects.get(order_id=order_id)
                            order.shiprocket_dashboard = True
                            order.save()

                            text = mail_otp.confirm_order_mail(email="ladoladhruv5218@gmail.com")
                            text
                            print(text)
                            mail_otp.send_mail(email="ladoladhruv5218@gmail.com",msg=text)
                            
                            print("shipment done")
                            try :
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
