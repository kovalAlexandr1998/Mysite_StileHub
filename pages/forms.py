from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Ваш email', 'class': 'form-control'}),
            'message': forms.Textarea(attrs={'placeholder': 'Ваше сообщение', 'class': 'form-control', 'rows': 5}),
        }
