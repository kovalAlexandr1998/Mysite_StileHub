from django import forms
from .models import ProductComment, Subscription, Order

class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ['user_name', 'user_email', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows':4, 'placeholder':'Ваш комментарий...'}),
            'user_name': forms.TextInput(attrs={'placeholder':'Ваше имя'}),
            'user_email': forms.EmailInput(attrs={'placeholder':'Ваш email'}),
        }

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Введите ваш email',
                'class': 'subscription-input'
            }),
        }

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        # Теперь только актуальные поля из модели
        fields = ['full_name', 'phone_number', 'email', 'novaposhta_branch']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Фамилия Имя Отчество'}),
            'phone_number': forms.TextInput(attrs={'placeholder': '+380 XX XXX XX XX'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@example.com'}),
            'novaposhta_branch': forms.TextInput(attrs={'placeholder': 'Отделение Новой Почты'}),
        }
