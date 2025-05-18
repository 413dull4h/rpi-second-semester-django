from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, AboutUs, Category, Service, 
    Contact, Users, Review, UserProfile
)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'category')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'category')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'address', 'profile_picture', 'category')}),
    )

@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name', 'description')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'updated_at')
    list_filter = ('category',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('created_at',)

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'category', 'is_active', 'created_at')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'email', 'phone')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'created_at', 'is_active')
    list_filter = ('rating', 'is_active', 'created_at')
    search_fields = ('name', 'comment')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_status', 'is_email_verified', 'created_at')
    list_filter = ('account_status', 'is_email_verified')
    search_fields = ('user__username', 'phone_number', 'address')