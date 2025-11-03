from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


# -------------------- Категории --------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL (slug)")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:category_detail', args=[self.slug])


# -------------------- Товары --------------------
class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
        null=True,
        blank=True
    )
    name = models.CharField(max_length=200, verbose_name="Название товара")
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    available = models.BooleanField(default=True, verbose_name="В наличии")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')
    alt_text = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Фото товара"
        verbose_name_plural = "Галерея фото"

    def __str__(self):
        return f"{self.product.name} - {self.id}"


class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField(max_length=100, verbose_name="Название характеристики")
    value = models.CharField(max_length=255, verbose_name="Значение характеристики")

    class Meta:
        verbose_name = "Характеристика товара"
        verbose_name_plural = "Характеристики товара"

    def __str__(self):
        return f"{self.product.name} - {self.name}"



class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size = models.CharField(max_length=10, verbose_name="Размер")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество на складе")

    class Meta:
        verbose_name = "Размер товара"
        verbose_name_plural = "Размеры товара"

    def __str__(self):
        return f"{self.product.name} - {self.size}"




# -------------------- Заказы --------------------
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    full_name = models.CharField(max_length=100, verbose_name="ФИО", default="не указано")
    phone_number = models.CharField(max_length=20, verbose_name="Телефон", default="не указан")
    email = models.EmailField(verbose_name="Email", default="example@example.com")
    novaposhta_branch = models.CharField(max_length=100, verbose_name="Отделение Новой Почты", default="не указано")
    status = models.CharField(max_length=20, default='Ожидает', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f'Заказ #{self.id} от {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Товар заказа"
        verbose_name_plural = "Товары заказа"

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
# -------------------- Корзина --------------------
# shop/models.py

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Корзина"

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments', verbose_name="Товар")
    user_name = models.CharField(max_length=100, verbose_name="Имя")
    user_email = models.EmailField(verbose_name="Email")
    text = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    approved = models.BooleanField(default=True, verbose_name="Одобрен")

    class Meta:
        verbose_name = "Комментарий к товару"
        verbose_name_plural = "Комментарии к товарам"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user_name} - {self.product.name}"


class Subscription(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата подписки")

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ['-created_at']

    def __str__(self):
        return self.email
