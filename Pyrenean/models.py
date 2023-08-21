from django.db import models


class Mens(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    size = models.CharField(max_length=4)
    color = models.CharField(max_length=10)
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/Mens/")
    created_on = models.DateTimeField(auto_now_add=True)


class Womens(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    size = models.CharField(max_length=4)
    color = models.CharField(max_length=10)
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/Womens/")
    created_on = models.DateTimeField(auto_now_add=True)


class Kides(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    size = models.CharField(max_length=4)
    color = models.CharField(max_length=10)
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/Kides/")
    created_on = models.DateTimeField(auto_now_add=True)


class CartModel(models.Model):
    id = models.AutoField
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    size = models.CharField(max_length=4)
    color = models.CharField(max_length=10)
    discount = models.PositiveIntegerField()
    slug = models.SlugField(unique=True, max_length=255)
    quantity = models.IntegerField(default=0)
    picture = models.ImageField(upload_to="static/images/CartModules/")
    created_on = models.DateTimeField(auto_now_add=True)


class ContactModel(models.Model):
    id = models.AutoField
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
