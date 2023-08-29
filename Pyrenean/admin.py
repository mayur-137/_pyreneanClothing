from django.contrib import admin
from .models import Mens, Women, Kid, CartModel, ContactModel, user_data, ProductBuyDetails


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "building", "street", "street", 'area', 'pincode', 'city']


class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "price", "discount", "slug", "max_quantity", "picture",
                    "created_on"]


admin.site.register(Mens, AuthorAdmin)
admin.site.register(Women, AuthorAdmin)
admin.site.register(Kid, AuthorAdmin)
admin.site.register(CartModel, AuthorAdmin)

admin.site.register(user_data, UserAdmin)


@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "created_on"]


@admin.register(ProductBuyDetails)
class ProductBuyDetailsAdmin(admin.ModelAdmin):
    list_display = ["id", "slug"]
