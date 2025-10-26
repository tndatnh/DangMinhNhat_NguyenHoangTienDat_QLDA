from django.contrib import admin
from .models import Fruit
from .models import Order, OrderItem

@admin.register(Fruit)
class FruitAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    list_filter = ('created_at',)
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