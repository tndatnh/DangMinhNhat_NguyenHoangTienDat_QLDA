from django.urls import path
from . import views

urlpatterns = [
    path('', views.fruit_list, name='fruit_list'),
    path('add-to-cart/<int:fruit_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('remove-from-cart/<int:fruit_id>/', views.remove_from_cart, name='remove_from_cart'),  
    path('checkout/', views.checkout, name='checkout'),
    path('fruit/<int:fruit_id>/', views.fruit_detail, name='fruit_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('orders/', views.order_history, name='order_history'),
    path('cart/update/<int:fruit_id>/<str:action>/', views.update_cart, name='update_cart'),
    
    # Dashboard & Quản lý (đã đổi tiền tố từ /admin/ → /dashboard/)
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/users/', views.user_management, name='user_management'),
    path('dashboard/users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    
    # Quản lý trái cây
    path('dashboard/fruits/', views.fruit_management, name='fruit_management'),
    path('dashboard/fruits/create/', views.fruit_create, name='fruit_create'),
    path('dashboard/fruits/edit/<int:fruit_id>/', views.fruit_update, name='fruit_update'),
    path('dashboard/fruits/delete/<int:fruit_id>/', views.fruit_delete, name='fruit_delete'),

    # Quản lý đơn hàng
    path('dashboard/orders/', views.order_management, name='order_management'),
    path('dashboard/orders/<int:order_id>/', views.order_detail_admin, name='order_detail_admin'),

    path('order/success/<int:order_id>/', views.order_success, name='order_success'),
]