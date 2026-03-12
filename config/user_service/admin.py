from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SellerProfile


class SellerProfileInline(admin.StackedInline):
    model = SellerProfile
    can_delete = False
    extra = 0


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "phone",
        "is_staff",
        "is_active",
        "is_seller",
    )
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name", "phone")
    ordering = ("email",)
    inlines = [SellerProfileInline]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone", "address", "date_of_birth")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Добавляем computed поле, чтобы сразу видеть, является ли пользователь продавцом
    def is_seller(self, obj):
        return hasattr(obj, "seller_profile")
    is_seller.boolean = True
    is_seller.short_description = "Seller"


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "store_name", "user_email", "created_at")
    search_fields = ("store_name", "user__email")
    list_filter = ("created_at",)

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = "User Email"

