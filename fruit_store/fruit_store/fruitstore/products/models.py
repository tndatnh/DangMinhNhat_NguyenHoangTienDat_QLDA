from django.db import models
from django.utils import timezone

class Fruit(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên trái cây")
    description = models.TextField(verbose_name="Mô tả")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá (VND/kg)")
    stock = models.PositiveIntegerField(default=0, verbose_name="Tồn kho (kg)")
    image = models.ImageField(upload_to='fruits/', blank=True, null=True, verbose_name="Ảnh")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Trái cây"
        verbose_name_plural = "Trái cây"

class Order(models.Model):
    customer_name = models.CharField(max_length=100, verbose_name="Họ và tên")
    phone = models.CharField(max_length=15, verbose_name="Số điện thoại")
    address = models.TextField(verbose_name="Địa chỉ giao hàng")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Tổng tiền")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Thời gian đặt")

    def __str__(self):
        return f"Đơn #{self.id} - {self.customer_name}"

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    fruit_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.fruit_name} x{self.quantity}"