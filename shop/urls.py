from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.catalog, name='shop_catalog'),  # Главная страница каталога
    path('cart/', views.cart_view, name='cart'),  # Корзина
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),  # Добавить в корзину
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),  # Удалить из корзины
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),  # Категория
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),  # Товар
    path('order/create/', views.order_create, name='order_create'),
    path('order/confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),

]
