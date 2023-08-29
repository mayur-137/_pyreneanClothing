from django.db import models
import uuid
from multiupload.fields import MultiFileField

SIZE_CHOICES = (
    ('Small', 'S'),
    ('Medium', 'M'),
    ('Large', 'L'),
    ('Extra Large', 'XL'),
    ('Very Extra Large', 'XXL')
)


class Mens(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)
    description = models.TextField(max_length=255)
    price = models.IntegerField()
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, default='Medium')
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    max_quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/Mens/", default="")
    created_on = models.DateTimeField(auto_now_add=True)


class Women(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)
    description = models.TextField(max_length=255)
    price = models.IntegerField()
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, default='Medium')
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    max_quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/Womens/")
    created_on = models.DateTimeField(auto_now_add=True)


class Kid(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=55)
    description = models.TextField(max_length=255)
    price = models.IntegerField()
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, default='Small')
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    max_quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/Kides/")
    created_on = models.DateTimeField(auto_now_add=True)


class CartModel(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=55)
    description = models.TextField(max_length=255)
    price = models.IntegerField()
    size = models.CharField(max_length=20)
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    max_quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/CartModules/")
    created_on = models.DateTimeField(auto_now_add=True)


class ContactModel(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=25)
    email = models.EmailField()
    message = models.TextField(max_length=4000)
    created_on = models.DateTimeField(auto_now_add=True)


class user_data(models.Model):
    id = models.AutoField
    email = models.EmailField(max_length=100)
    building = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)


class ProductBuyDetails(models.Model):
    id = models.AutoField
    email = models.EmailField()
    slug = models.SlugField(unique=True, max_length=255)
