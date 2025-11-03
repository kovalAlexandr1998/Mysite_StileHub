from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, CartItem, Category, Subscription
from django.contrib.auth.decorators import login_required
from .forms import ProductCommentForm, SubscriptionForm, OrderCreateForm
from django.contrib import messages
from .models import OrderItem, Order

# ======= Каталог =======
def catalog(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    return render(request, 'shop/catalog.html', {
        'categories': categories,
        'products': products
    })

# ======= Категория =======
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(available=True)
    categories = Category.objects.all()
    return render(request, 'shop/category_detail.html', {
        'category': category,
        'products': products,
        'categories': categories
    })

# ======= Детальная страница товара =======
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    comments = product.comments.filter(approved=True)

    if request.method == 'POST':
        form = ProductCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('shop:product_detail', slug=product.slug)
    else:
        form = ProductCommentForm()

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'comments': comments,
        'form': form
    })

# ======= Корзина =======
@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price for item in items)
    return render(request, 'shop/cart.html', {'items': items, 'total': total})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('shop:cart')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return redirect('shop:cart')

# ======= Подписка =======
def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not Subscription.objects.filter(email=email).exists():
                form.save()
                messages.success(request, 'Вы успешно подписались на обновления!')
            else:
                messages.info(request, 'Вы уже подписаны на обновления.')
        else:
            messages.error(request, 'Некорректный email, попробуйте снова.')
    return redirect(request.META.get('HTTP_REFERER', '/'))

# ======= Оформление заказа =======
@login_required
def order_create(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price for item in items)

    if not items.exists():
        return redirect('shop:cart')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.total_price
                )
            items.delete()  # очищаем корзину
            return redirect('shop:order_confirmation', order_id=order.id)
    else:
        form = OrderCreateForm()

    return render(request, 'shop/order_create.html', {
        'items': items,
        'total': total,
        'form': form
    })

@login_required
def order_confirmation(request, order_id):
    return render(request, 'shop/order_confirmation.html', {'order_id': order_id})
