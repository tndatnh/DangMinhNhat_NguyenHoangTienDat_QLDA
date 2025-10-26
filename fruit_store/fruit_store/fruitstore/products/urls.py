from django.urls import path
from . import views

urlpatterns = [
    path('', views.fruit_list, name='fruit_list'),
    path('add-to-cart/<int:fruit_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('remove-from-cart/<str:fruit_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('fruit/<int:fruit_id>/', views.fruit_detail, name='fruit_detail'),
]