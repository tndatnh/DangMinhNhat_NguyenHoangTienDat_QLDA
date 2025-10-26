from django import forms
from django.contrib.auth.models import User
from .models import Fruit

class FruitForm(forms.ModelForm):
    class Meta:
        model = Fruit
        fields = ['name', 'description', 'price', 'stock', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CheckoutForm(forms.Form):
    customer_name = forms.CharField(
        max_length=100,
        label="Họ và tên",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=15,
        label="Số điện thoại",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        label="Địa chỉ giao hàng",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    payment_method = forms.ChoiceField(
        choices=[
            ('cod', 'Thanh toán khi nhận hàng (COD)'),
            ('bank', 'Chuyển khoản ngân hàng'),
        ],
        label="Hình thức thanh toán",
        widget=forms.RadioSelect,
        initial='cod'
    )

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }