from django.db import models
import uuid


class Mens(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)
    description = models.TextField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    stock = models.BooleanField(default=True)
    picture = models.ImageField(upload_to="static/images/Mens/", default="")
    picture_1 = models.ImageField(upload_to="static/images/Mens/", default="")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Price: {self.slug})"
    
    def get_sizes(self):
        # Use the related_name defined in the ForeignKey to access the sizes
        return self.size_set.all()

    def __str__(self):
        return f"{self.name} (Price: {self.slug})"


class Women(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)
    description = models.TextField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    stock = models.BooleanField(default=True)
    picture = models.ImageField(upload_to="static/images/Womens/")
    picture_1 = models.ImageField(upload_to="static/images/Womens/", default="")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Price: {self.slug})"


class UniSex(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)
    description = models.TextField(max_length=255)
    price = models.IntegerField()
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    picture = models.ImageField(upload_to="static/images/UniSex/")
    picture_1 = models.ImageField(upload_to="static/images/UniSex/", default="")
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (Price: {self.slug})"


class CartModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_id = models.CharField(max_length=100, null=False)
    size_id = models.CharField(max_length=100, null=True, default=None)
    # name = models.CharField(max_length=55)
    email = models.EmailField(unique=False, max_length=100, default="")
    # description = models.TextField(max_length=255)
    price = models.IntegerField(default=0)
    # discount = models.PositiveIntegerField()
    # slug = models.SlugField(unique=True, max_length=255)
    # stock = models.BooleanField(default=True)
    size = models.CharField(max_length=4, default="", null=True)
    quantity = models.IntegerField(default=0, null=True)
    # picture = models.ImageField(upload_to="static/images/CartModules/")
    # picture_1 = models.ImageField(upload_to="static/images/CartModules/", default="")
    created_on = models.DateTimeField(auto_now_add=True)


class ContactModel(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
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
    men = models.ForeignKey(Mens, on_delete=models.SET_NULL, db_column="", null=True, blank=True)
    kid = models.ForeignKey(UniSex, on_delete=models.SET_NULL, db_column="", null=True, blank=True)
    women = models.ForeignKey(Women, on_delete=models.SET_NULL, db_column="", null=True, blank=True)

    def __str__(self):
        return f"{self.size} (Quantity: {self.quantity})"


class user_email(models.Model):
    email = models.CharField(max_length=100)
    otp = models.IntegerField()
    
class user_data(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=100)
    building = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100,default="GUJRAT")
    phone_number = models.CharField(max_length=100)



class cart_data(models.Model):
    order_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    address_1 = models.CharField(max_length=1000,default="INDIA")
    # product_picture = models.ImageField(upload_to="static/images/VitaminCapsules/",default="")
    products_detail = models.CharField(max_length=1000,default='empty')
    order_total = models.IntegerField()

class final_order(models.Model):
    order_id = models.AutoField(primary_key=True)
    email = models.EmailField()
    address = models.CharField(max_length=1000,default="INDIA")
    products_detail = models.CharField(max_length=1000,default='empty')
    order_total = models.IntegerField()
    shiprocket_dashboard = models.BooleanField(default=False)    