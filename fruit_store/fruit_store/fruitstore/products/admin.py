from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Fruit, Order, OrderItem

# ========== Các model của bạn ==========
@admin.register(Fruit)
class FruitAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'phone', 'total_amount', 'created_at')
    inlines = [OrderItemInline]
    readonly_fields = ('created_at',)

# ========== MỞ RỘNG USER ADMIN ==========
class UserAdmin(BaseUserAdmin):
    # Thêm các trường bạn muốn hiển thị
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    
    # Tùy chỉnh form chỉnh sửa
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Thông tin cá nhân', {'fields': ('first_name', 'last_name', 'email')}),
        ('Quyền', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Ngày', {'fields': ('last_login', 'date_joined')}),
    )

# Hủy đăng ký User mặc định và đăng ký lại với class mới
admin.site.unregister(User)
admin.site.register(User, UserAdmin)