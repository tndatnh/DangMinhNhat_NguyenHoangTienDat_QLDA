from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Fruit, Order, OrderItem, User
from .forms import CheckoutForm
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum, Count
from datetime import datetime, timedelta
from .forms import UserEditForm
from .forms import FruitForm

@user_passes_test(lambda u: u.is_staff)
def order_detail_admin(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Tính thành tiền cho từng item
    for item in order.items.all():
        item.total_price = item.price * item.quantity
    return render(request, 'products/order_detail_admin.html', {'order': order})

@user_passes_test(lambda u: u.is_staff)
def order_management(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'products/order_management.html', {'orders': orders})

@user_passes_test(lambda u: u.is_staff)
def order_detail_admin(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'products/order_detail_admin.html', {'order': order})

@user_passes_test(lambda u: u.is_staff)
def fruit_management(request):
    fruits = Fruit.objects.all()
    return render(request, 'products/fruit_management.html', {'fruits': fruits})

@user_passes_test(lambda u: u.is_staff)
def fruit_create(request):
    if request.method == 'POST':
        form = FruitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Đã thêm trái cây mới!")
            return redirect('fruit_management')
    else:
        form = FruitForm()
    return render(request, 'products/fruit_form.html', {'form': form, 'title': 'Thêm trái cây'})

@user_passes_test(lambda u: u.is_staff)
def fruit_update(request, fruit_id):
    fruit = get_object_or_404(Fruit, id=fruit_id)
    if request.method == 'POST':
        form = FruitForm(request.POST, request.FILES, instance=fruit)
        if form.is_valid():
            form.save()
            messages.success(request, f"Đã cập nhật {fruit.name}!")
            return redirect('fruit_management')
    else:
        form = FruitForm(instance=fruit)
    return render(request, 'products/fruit_form.html', {'form': form, 'title': 'Chỉnh sửa trái cây'})

@user_passes_test(lambda u: u.is_staff)
def fruit_delete(request, fruit_id):
    fruit = get_object_or_404(Fruit, id=fruit_id)
    if request.method == 'POST':
        fruit.delete()
        messages.success(request, f"Đã xóa {fruit.name}!")
        return redirect('fruit_management')
    return render(request, 'products/fruit_confirm_delete.html', {'fruit': fruit})

# Chỉ admin mới được truy cập
@user_passes_test(lambda u: u.is_staff)
def user_management(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'products/user_management.html', {'users': users})

@user_passes_test(lambda u: u.is_staff)
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Đã cập nhật tài khoản '{user.username}'!")
            return redirect('user_management')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'products/edit_user.html', {'form': form, 'user': user})

# Chỉ admin mới được truy cập
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    # Thống kê cơ bản
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    total_fruits = Fruit.objects.count()
    total_users = User.objects.count()

    # Đơn hàng trong 7 ngày gần nhất
    last_week = datetime.now() - timedelta(days=7)
    recent_orders = Order.objects.filter(created_at__gte=last_week).count()

    # Top 5 sản phẩm bán chạy
    top_fruits = OrderItem.objects.values('fruit_name').annotate(
        total_sold=Sum('quantity')
    ).order_by('-total_sold')[:5]

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_fruits': total_fruits,
        'total_users': total_users,
        'recent_orders': recent_orders,
        'top_fruits': top_fruits,
    }
    return render(request, 'products/admin_dashboard.html', context)

# ========== Đơn hàng ==========
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'products/order_history.html', {'orders': orders})

# ========== Giỏ hàng ==========
def add_to_cart(request, fruit_id):
    cart = request.session.get('cart', {})
    
    # Chuẩn hóa cart trước (phòng trường hợp session cũ)
    new_cart = {}
    for k, v in cart.items():
        try:
            new_cart[int(k)] = v
        except (ValueError, TypeError):
            new_cart[k] = v
    cart = new_cart
    
    try:
        fruit = Fruit.objects.get(id=fruit_id)
    except Fruit.DoesNotExist:
        messages.error(request, "Trái cây không tồn tại!")
        return redirect('fruit_list')
    
    if fruit_id in cart:
        if cart[fruit_id]['quantity'] < fruit.stock:
            cart[fruit_id]['quantity'] += 1
            messages.success(request, f"Đã thêm thêm {fruit.name} vào giỏ!")
        else:
            messages.warning(request, f"Số lượng {fruit.name} trong kho không đủ!")
    else:
        cart[fruit_id] = {
            'name': fruit.name,
            'price': float(fruit.price),
            'quantity': 1,
            'stock': fruit.stock,
        }
        messages.success(request, f"Đã thêm {fruit.name} vào giỏ!")
    
    request.session['cart'] = cart
    return redirect('fruit_list')

def cart_detail(request):
    cart = request.session.get('cart', {})
    
    # CHUYỂN TOÀN BỘ KEY VỀ INT (nếu là string)
    new_cart = {}
    for k, v in cart.items():
        try:
            new_cart[int(k)] = v
        except (ValueError, TypeError):
            new_cart[k] = v  # giữ nguyên nếu không chuyển được
    
    # Lưu lại cart đã chuẩn hóa
    request.session['cart'] = new_cart
    
    total = 0
    for item in new_cart.values():
        item['total_price'] = item['price'] * item['quantity']
        total += item['total_price']
    return render(request, 'products/cart_detail.html', {'cart': new_cart, 'total': total})

def update_cart(request, fruit_id, action):
    cart = request.session.get('cart', {})
    
    # Chuẩn hóa cart: chuyển key sang int
    new_cart = {}
    for k, v in cart.items():
        try:
            new_cart[int(k)] = v
        except (ValueError, TypeError):
            new_cart[k] = v
    cart = new_cart
    
    print("=== DEBUG update_cart ===")
    print("fruit_id từ URL:", fruit_id, type(fruit_id))
    print("Keys trong cart:", list(cart.keys()))
    
    if fruit_id not in cart:
        messages.error(request, "Sản phẩm không có trong giỏ hàng.")
        return redirect('cart_detail')
    
    fruit = Fruit.objects.get(name=cart[fruit_id]['name'])
    
    if action == 'increase':
        if cart[fruit_id]['quantity'] < fruit.stock:
            cart[fruit_id]['quantity'] += 1
            messages.success(request, f"Đã tăng số lượng {fruit.name}.")
        else:
            messages.warning(request, f"Số lượng {fruit.name} trong kho không đủ!")
    elif action == 'decrease':
        if cart[fruit_id]['quantity'] > 1:
            cart[fruit_id]['quantity'] -= 1
            messages.success(request, f"Đã giảm số lượng {fruit.name}.")
        else:
            del cart[fruit_id]
            request.session['cart'] = cart
            messages.success(request, "Đã xóa sản phẩm khỏi giỏ hàng.")
            return redirect('cart_detail')
    
    request.session['cart'] = cart
    return redirect('cart_detail')

def remove_from_cart(request, fruit_id):
    cart = request.session.get('cart', {})
    
    # Chuẩn hóa cart
    new_cart = {}
    for k, v in cart.items():
        try:
            new_cart[int(k)] = v
        except (ValueError, TypeError):
            new_cart[k] = v
    cart = new_cart
    
    if fruit_id in cart:
        del cart[fruit_id]
        request.session['cart'] = cart
        messages.success(request, "Đã xóa sản phẩm khỏi giỏ hàng.")
    else:
        messages.error(request, "Sản phẩm không có trong giỏ hàng.")
    return redirect('cart_detail')

# ========== Thanh toán ==========
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Giỏ hàng của bạn đang trống!")
        return redirect('fruit_list')
    
    total = sum(float(item['price']) * item['quantity'] for item in cart.values())

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Kiểm tra tồn kho TRƯỚC khi tạo đơn
            for item in cart.values():
                try:
                    fruit = Fruit.objects.get(name=item['name'])
                    if fruit.stock < item['quantity']:
                        messages.error(request, f"Sản phẩm '{fruit.name}' không đủ hàng (còn {fruit.stock} kg)!")
                        return redirect('cart_detail')
                except Fruit.DoesNotExist:
                    messages.error(request, f"Sản phẩm '{item['name']}' không tồn tại trong hệ thống!")
                    return redirect('cart_detail')

            # Tạo đơn hàng
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                customer_name=form.cleaned_data['customer_name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                total_amount=total
            )
            
            # Tạo chi tiết đơn + TRỪ TỒN KHO
            for item in cart.values():
                OrderItem.objects.create(
                    order=order,
                    fruit_name=item['name'],
                    price=item['price'],
                    quantity=item['quantity']
                )
                fruit = Fruit.objects.get(name=item['name'])
                fruit.stock -= item['quantity']
                fruit.save()
            
            del request.session['cart']
            messages.success(request, f"Đặt hàng thành công! Mã đơn: #{order.id}")
            return redirect('fruit_list')
    else:
        form = CheckoutForm()
    
    return render(request, 'products/checkout.html', {'form': form, 'cart': cart, 'total': total})

# ========== Xem sản phẩm ==========
def fruit_list(request):
    fruits = Fruit.objects.all()
    return render(request, 'products/fruit_list.html', {'fruits': fruits})

def fruit_detail(request, fruit_id):
    fruit = get_object_or_404(Fruit, id=fruit_id)
    return render(request, 'products/fruit_detail.html', {'fruit': fruit})

# ========== Tài khoản ==========
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Tài khoản '{username}' đã được tạo thành công!")
            login(request, user)
            return redirect('fruit_list')
    else:
        form = UserCreationForm()
    return render(request, 'products/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('fruit_list')
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng.")
    return render(request, 'products/login.html')

def user_logout(request):
    logout(request)
    messages.info(request, "Bạn đã đăng xuất.")
    return redirect('fruit_list')