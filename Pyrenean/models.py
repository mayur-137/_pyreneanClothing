from django.db import models
import uuid


class ContactModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=25)
    email = models.EmailField(unique=False)
    message = models.TextField(max_length=4000)
    created_on = models.DateTimeField(auto_now_add=True)


class user_data(models.Model):
    id = models.AutoField
    email = models.EmailField(max_length=100, unique=True)
    building = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)


class user_email(models.Model):
    email = models.CharField(max_length=100)
    otp = models.IntegerField()


class user_address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=100)
    building = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, default="GUJRAT")
    phone_number = models.CharField(max_length=100)


class cart_data(models.Model):
    order_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    address_1 = models.CharField(max_length=1000, default="INDIA")
    products_detail = models.JSONField(null=True)
    order_total = models.IntegerField(null=True, default=0)

    def __str__(self):
        return f"{self.products_detail}, {self.order_total}"


class final_order(models.Model):
    order_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    address = models.CharField(max_length=1000, default="INDIA")
    products_detail = models.CharField(max_length=1000, default='empty')
    order_total = models.IntegerField()
    shiprocket_dashboard = models.BooleanField(default=False)
    link_id = models.CharField(max_length=1000,default=000)


class Product_Details(models.Model):
    CATEGORY_CHOICES = [
        ('Mens', 'Mens'),
        ('UniSex', 'UniSex'),
        ('Women', 'Women'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=5000)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    picture = models.ImageField(upload_to="static/images/Product_images/")
    picture_1 = models.ImageField(upload_to="static/images/Product_images/")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Extra Extra Large'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    size = models.CharField(max_length=255, choices=SIZE_CHOICES)
    quantity = models.IntegerField(default=0)
    product = models.ForeignKey(Product_Details, on_delete=models.CASCADE, default="")

    # kid = models.ForeignKey(UniSex, on_delete=models.SET_NULL, db_column="", null=True, blank=True)
    # women = models.ForeignKey(Women, on_delete=models.SET_NULL, db_column="", null=True, blank=True)

    def __str__(self):
        return f"{self.size} (Quantity: {self.quantity})"


class WishList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.CharField(max_length=50, unique=True)


class SubscribeNow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    email = models.EmailField(default="")
    discount_percent = models.IntegerField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
