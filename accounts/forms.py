from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class RegistrationForm(forms.ModelForm):
    """Каттоо формасы: Имя, Email жана Пароль менен"""
    
    # Бул талаа интерфейсте колдонуучунун атын көрсөтүү үчүн
    first_name = forms.CharField(
        label='Имя',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Мисалы: Намазбек'
        })
    )
    
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.com'
        })
    )
    
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль түзүңүз'
        })
    )
    
    password2 = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Паролду кайталаңыз'
        })
    )
    
    class Meta:
        model = User
        # 'first_name' базадагы моделдин талаасы, аны сөзсүз кошобуз
        fields = ('first_name', 'email', 'password1', 'password2')

    def clean_email(self):
        """Негизги текшерүү: Аккаунттун уникалдуулугу почта менен аныкталат"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Бул почта менен аккаунт мурунтан бар. Башка почта жазыңыз же кириңиз.')
        return email

    def clean(self):
        """Паролдорду салыштыруу"""
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 != p2:
            raise ValidationError('Паролдор окшош эмес. Кайра текшериңиз.')
        return cleaned_data

    def save(self, commit=True):
        """Маалыматты базага сактоо"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        
        # Аккаунттун уникалдуу логини (username) катары почтаны сактайбыз
        user.username = self.cleaned_data['email']
        
        # Аты (first_name) автоматтык түрдө Meta-fields аркылуу сакталат
        
        if commit:
            user.save()
        return user



class LoginForm(forms.Form):
    """Кирүү формасы"""
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
    )