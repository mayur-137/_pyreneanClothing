from django.contrib import admin
from .models import ContactModel, user_address, Size, user_email, cart_data, final_order, Product_Details, WishList, \
    SubscribeNow, PromoCode


# Register your models here.# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "building", "street", "street", 'area', 'pincode', 'city', 'state']


admin.site.register(user_address, AuthorAdmin)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category", "description", "price", "discount", "slug", "picture",
                    "created_on"]


# admin.site.register(Mens, AuthorAdmin)
# admin.site.register(Women, AuthorAdmin)
# admin.site.register(UniSex, AuthorAdmin)
admin.site.register(Product_Details, AuthorAdmin)


@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "created_on"]


@admin.register(Size)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ["id", "size", "quantity", "product"]


# @admin.register(CartModel)
# class ModelNameAdmin(admin.ModelAdmin):
#     list_display = ["id", "product_id", "quantity", "size", "email"]


class AuthorAdmin_user_email(admin.ModelAdmin):
    list_display = ["email", "otp"]


admin.site.register(user_email, AuthorAdmin_user_email)


@admin.register(cart_data)
class AuthorAdmin_order(admin.ModelAdmin):
    list_display = ["order_id", "email", "address_1", "products_detail", "order_total"]


# admin.site.register(orders,AuthorAdmin_order)

@admin.register(final_order)
class AuthorAdmin_final_order(admin.ModelAdmin):
    list_display = ["order_id", "email", "address", "products_detail", "order_total", "shiprocket_dashboard"]


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ["id", "product_id"]


@admin.register(SubscribeNow)
class WishListAdmin(admin.ModelAdmin):
    list_display = ["id", "email"]


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ["active", "code", "discount_percent"]
