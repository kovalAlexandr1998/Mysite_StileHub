from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserForm, ProfileForm
from shop.models import Order  # заменить на свою модель заказов


# ---------------- Регистрация ----------------
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # сразу логиним пользователя
            messages.success(request, "Регистрация успешна!")
            return redirect('profile')  # перенаправляем в профиль
        else:
            messages.error(request, "Исправьте ошибки в форме.")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


# ---------------- Вход по email ----------------
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            user_auth = authenticate(request, username=user.username, password=password)
            if user_auth:
                login(request, user_auth)
                messages.success(request, f"Добро пожаловать, {user.first_name}!")
                return redirect('profile')

        messages.error(request, "Неправильный email или пароль.")

    return render(request, 'accounts/login.html')


# ---------------- Выход ----------------
def logout_user(request):
    logout(request)
    return redirect('index')


# ---------------- Профиль ----------------
@login_required
def profile(request):
    user = request.user
    profile = user.profile

    # исправлено поле сортировки
    orders = Order.objects.filter(user=user).order_by('-created_at') if hasattr(user, 'order_set') else []

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Профиль успешно обновлён!")
            return redirect('profile')
        else:
            messages.error(request, "Исправьте ошибки в форме.")
    else:
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=profile)

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'orders': orders
    })
