from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# ---------------- Регистрационная форма ----------------
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Имя', 'class': 'input-field'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Фамилия', 'class': 'input-field'}))
    middle_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Отчество', 'class': 'input-field'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'input-field'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'input-field'}))
    password2 = forms.CharField(label="Подтверждение пароля", widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль', 'class': 'input-field'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.middle_name = self.cleaned_data.get('middle_name', '')
            profile.save()
        return user

# ---------------- Форма User (редактирование имени/фамилии) ----------------
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Фамилия'}),
        }

# ---------------- Форма профиля ----------------
class ProfileForm(forms.ModelForm):
    birth_year = forms.DateField(
        label="Дата рождения",
        required=False,
        widget=forms.DateInput(
            attrs={
                'class': 'input-field',
                'placeholder': 'ДД.ММ.ГГГГ',
                'type': 'text'  # чтобы можно было вводить дату вручную
            },
            format='%d.%m.%Y'
        ),
        input_formats=['%d.%m.%Y']
    )

    class Meta:
        model = Profile
        fields = ['middle_name', 'birth_year', 'city', 'avatar', 'phone', 'address', 'language']
        widgets = {
            'middle_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Отчество'}),
            'city': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Город'}),
            'avatar': forms.FileInput(attrs={'class': 'input-field', 'placeholder': 'Сменить аватарку'}),
            'phone': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Телефон'}),
            'address': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Адрес'}),
            'language': forms.Select(attrs={'class': 'input-field'}),
        }
