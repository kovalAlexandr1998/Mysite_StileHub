from django.shortcuts import render, redirect
from shop.forms import SubscriptionForm
from .forms import ContactForm

# ======= Главная страница =======
def index(request):
    form = SubscriptionForm()
    success_message = ''
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            success_message = 'Вы успешно подписались на обновления!'
            form = SubscriptionForm()  # очистка формы после отправки
    return render(request, 'pages/index.html', {
        'form': form,
        'success_message': success_message
    })

# ======= О сайте =======
def about(request):
    return render(request, 'pages/about.html')

# ======= Контакты =======
def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'pages/contacts.html', {'form': ContactForm(), 'success': True})
    else:
        form = ContactForm()
    return render(request, 'pages/contacts.html', {'form': form})
