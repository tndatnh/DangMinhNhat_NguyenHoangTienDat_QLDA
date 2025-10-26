from django import forms

class CheckoutForm(forms.Form):
    customer_name = forms.CharField(
        max_length=100,
        label="Họ và tên",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nhập họ và tên'})
    )
    phone = forms.CharField(
        max_length=15,
        label="Số điện thoại",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0901234567'})
    )
    address = forms.CharField(
        label="Địa chỉ giao hàng",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Số nhà, đường, quận, thành phố'})
    )