from django.contrib import admin
from .models import Product, Order, CartItem, Category, ProductImage, ProductSpecification, ProductSize
from .models import ProductComment
from .models import Subscription



# -------------------- Вставки для галереи, характеристик и размеров --------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 10  # максимум 10 фото

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1

# -------------------- Админка для Product --------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available', 'category')
    list_filter = ('available', 'category')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductSpecificationInline, ProductSizeInline]

# -------------------- Админка для Category --------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

# -------------------- Админка для Order --------------------
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_products', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'items__product__name')

    def get_products(self, obj):
        return ", ".join([f"{item.product.name} ({item.quantity})" for item in obj.items.all()])
    get_products.short_description = 'Товары'

# -------------------- Админка для CartItem --------------------
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    search_fields = ('user__username', 'product__name')
    list_filter = ('user',)

# -------------------- Админка для ProductImage, ProductSpecification и ProductSize (по желанию) --------------------
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image', 'alt_text')
    search_fields = ('product__name',)

@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'name', 'value')
    search_fields = ('product__name', 'name', 'value')

@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'quantity')
    search_fields = ('product__name', 'size')

@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'product', 'created_at', 'approved')
    list_filter = ('approved', 'created_at')
    search_fields = ('user_name', 'user_email', 'text', 'product__name')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    list_filter = ('created_at',)
