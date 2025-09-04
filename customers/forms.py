from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import Customer, Address


class CustomerRegistrationForm(UserCreationForm):
    """Customer registration form"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'input-field',
            'placeholder': 'Enter your email'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'First name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Last name'
        })
    )
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Phone number (optional)'
        })
    )
    accepts_marketing = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 rounded focus:ring-primary-500'
        })
    )
    
    class Meta:
        model = Customer
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2', 'accepts_marketing')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add CSS classes to username and password fields
        self.fields['username'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': 'Confirm password'
        })
        
        # Update field labels
        self.fields['username'].label = 'Username'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confirm Password'
        self.fields['accepts_marketing'].label = 'I would like to receive marketing emails'
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Customer.objects.filter(email=email).exists():
            raise ValidationError('A user with this email already exists.')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone = self.cleaned_data.get('phone', '')
        user.accepts_marketing = self.cleaned_data.get('accepts_marketing', False)
        
        if commit:
            user.save()
        return user


class CustomerLoginForm(AuthenticationForm):
    """Custom login form"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Username or email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-field',
            'placeholder': 'Password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 rounded focus:ring-primary-500'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username or Email'
        self.fields['password'].label = 'Password'
        self.fields['remember_me'].label = 'Remember me'
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        # Allow login with email or username
        if '@' in username:
            try:
                user = Customer.objects.get(email=username)
                return user.username
            except Customer.DoesNotExist:
                pass
        
        return username


class CustomerEditForm(forms.ModelForm):
    """Form for editing customer profile"""
    
    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'email', 'phone', 'date_of_birth', 'accepts_marketing')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input-field',
                'placeholder': 'Email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Phone number'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'input-field',
                'type': 'date'
            }),
            'accepts_marketing': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 rounded focus:ring-primary-500'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['accepts_marketing'].label = 'I would like to receive marketing emails'
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Customer.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('A user with this email already exists.')
        return email


class AddressForm(forms.ModelForm):
    """Form for managing customer addresses"""
    
    class Meta:
        model = Address
        fields = (
            'type', 'first_name', 'last_name', 'company', 'address_line_1', 
            'address_line_2', 'city', 'state', 'postal_code', 'country', 
            'phone', 'is_default'
        )
        widgets = {
            'type': forms.Select(attrs={
                'class': 'input-field'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'First name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Last name'
            }),
            'company': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Company (optional)'
            }),
            'address_line_1': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Street address'
            }),
            'address_line_2': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Apartment, suite, etc. (optional)'
            }),
            'city': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'State/Province'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'ZIP/Postal code'
            }),
            'country': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Country'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Phone number (optional)'
            }),
            'is_default': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-primary-600 bg-gray-100 border-gray-300 rounded focus:ring-primary-500'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_default'].label = 'Set as default address'