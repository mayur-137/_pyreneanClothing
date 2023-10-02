from django.contrib import admin
from .models import Mens, Women, UniSex, CartModel, ContactModel, user_data, Size


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "building", "street", "street", 'area', 'pincode', 'city']


class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "price", "discount", "slug", "picture",
                    "created_on"]


admin.site.register(Mens, AuthorAdmin)
admin.site.register(Women, AuthorAdmin)
admin.site.register(UniSex, AuthorAdmin)

admin.site.register(user_data, UserAdmin)


@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "created_on"]


@admin.register(Size)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ["size", "quantity", "men", "kid", "women"]


@admin.register(CartModel)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ["id", "product_id", "quantity", "size", "email"]
