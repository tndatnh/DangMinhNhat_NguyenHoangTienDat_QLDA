from django.shortcuts import render
from .models import Fruit
from django.shortcuts import redirect
from django.contrib import messages
from .forms import CheckoutForm
from .models import Fruit, Order, OrderItem
from django.shortcuts import get_object_or_404

def fruit_detail(request, fruit_id):
    fruit = get_object_or_404(Fruit, id=fruit_id)
    return render(request, 'products/fruit_detail.html', {'fruit': fruit})

def fruit_list(request):
    fruits = Fruit.objects.all()
    return render(request, 'products/fruit_list.html', {'fruits': fruits})

def add_to_cart(request, fruit_id):
    # Lấy giỏ hàng từ session (nếu chưa có thì tạo dict rỗng)
    cart = request.session.get('cart', {})
    
    # Lấy thông tin trái cây
    try:
        fruit = Fruit.objects.get(id=fruit_id)
    except Fruit.DoesNotExist:
        messages.error(request, "Trái cây không tồn tại!")
        return redirect('fruit_list')
    
    # Chuyển fruit_id thành chuỗi (session chỉ lưu key là string)
    fruit_id_str = str(fruit_id)
    
    if fruit_id_str in cart:
        # Nếu đã có trong giỏ → tăng số lượng (tối đa = tồn kho)
        if cart[fruit_id_str]['quantity'] < fruit.stock:
            cart[fruit_id_str]['quantity'] += 1
            messages.success(request, f"Đã thêm thêm {fruit.name} vào giỏ!")
        else:
            messages.warning(request, f"Số lượng {fruit.name} trong kho không đủ!")
    else:
        # Nếu chưa có → thêm mới
        cart[fruit_id_str] = {
            'name': fruit.name,
            'price': float(fruit.price),
            'quantity': 1,
            'stock': fruit.stock,
        }
        messages.success(request, f"Đã thêm {fruit.name} vào giỏ!")
    
    # Lưu lại giỏ hàng vào session
    request.session['cart'] = cart
    return redirect('fruit_list')

def cart_detail(request):
    cart = request.session.get('cart', {})
    total = 0
    for item in cart.values():
        item['total_price'] = item['price'] * item['quantity']
        total += item['total_price']
    return render(request, 'products/cart_detail.html', {'cart': cart, 'total': total})

def remove_from_cart(request, fruit_id):
    cart = request.session.get('cart', {})
    if fruit_id in cart:
        del cart[fruit_id]
        request.session['cart'] = cart
        messages.success(request, "Đã xóa sản phẩm khỏi giỏ hàng.")
    return redirect('cart_detail')

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Giỏ hàng của bạn đang trống!")
        return redirect('fruit_list')
    
    total = sum(float(item['price']) * item['quantity'] for item in cart.values())

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Tạo đơn hàng
            order = Order.objects.create(
                customer_name=form.cleaned_data['customer_name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                total_amount=total
            )
            # Tạo các mục trong đơn
            for item in cart.values():
                OrderItem.objects.create(
                    order=order,
                    fruit_name=item['name'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # Xoá giỏ hàng
            del request.session['cart']
            messages.success(request, f"Đặt hàng thành công! Mã đơn: #{order.id}")
            return redirect('fruit_list')
    else:
        form = CheckoutForm()
    
    return render(request, 'products/checkout.html', {'form': form, 'cart': cart, 'total': total})

def fruit_detail(request, fruit_id):
    fruit = get_object_or_404(Fruit, id=fruit_id)
    return render(request, 'products/fruit_detail.html', {'fruit': fruit})