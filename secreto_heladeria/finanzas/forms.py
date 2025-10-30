from django import forms
from django.forms.models import BaseInlineFormSet
from django.contrib.auth import get_user_model
from .models import Transaccion, Producto, Categoria, Profile 
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm

class TransaccionInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                monto = form.cleaned_data.get('monto')
                if monto is not None and monto <= 0:
                    raise ValidationError("El monto de cada transacción debe ser mayor a 0.")

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre',
            'categoria',
            'costo_unitario',
            'precio_venta',
            'stock',
            'activo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ej: Helado de Chocolate'}),
            'categoria': forms.Select(),
            'costo_unitario': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'precio_venta': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'stock': forms.NumberInput(attrs={'placeholder': '0'}),
            'activo': forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
             if hasattr(field.widget, 'attrs'):
                 field.widget.attrs.update({'class': 'form-input-css'})

class TransaccionForm(forms.ModelForm):
    tipo = forms.ChoiceField(
        choices=Transaccion.TIPOS,
        widget=forms.RadioSelect,
        required=True
    )

    class Meta:
        model = Transaccion
        fields = [
            'tipo',
            'producto',
            'categoria',
            'monto',
            'descripcion',
            'fecha',
        ]
        widgets = {
            'fecha': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'monto': forms.NumberInput(attrs={'placeholder': '0.00', 'step': '0.01'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Descripción breve'}),
            'producto': forms.Select(),
            'categoria': forms.Select(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].queryset = Categoria.objects.order_by('nombre')
        self.fields['producto'].queryset = Producto.objects.filter(activo=True).order_by('nombre')

        self.fields['producto'].required = False
        self.fields['categoria'].required = False
        self.fields['categoria'].empty_label = "Sin categoría"
        self.fields['producto'].empty_label = "Ninguno"

        if self.instance and self.instance.pk and self.instance.fecha:
           self.initial['fecha'] = self.instance.fecha.strftime('%Y-%m-%dT%H:%M')
        else:
           self.initial['fecha'] = timezone.now().strftime('%Y-%m-%dT%H:%M')

        for field_name, field in self.fields.items():
             if hasattr(field.widget, 'attrs'):
                 field.widget.attrs.update({'class': 'form-input-css'})

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        producto = cleaned_data.get('producto')
        categoria = cleaned_data.get('categoria')
        descripcion = cleaned_data.get('descripcion')

        if producto and tipo == 'gasto':
            self.add_error('tipo', 'Si seleccionas un producto, debe ser un Ingreso (venta).')

        if not producto and not categoria and not descripcion:
             raise ValidationError('Debes seleccionar un Producto, una Categoría o ingresar una Descripción.')

        return cleaned_data

User = get_user_model()

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu email'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Este email ya está en uso por otro usuario.")
        return email

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['foto']
        widgets = {
            'foto': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}), 
        }

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Elige un nombre de usuario',
            'email': 'tu@correo.com',
            'first_name': 'Tu nombre',
            'last_name': 'Tu apellido',
            'password': 'Crea una contraseña segura',
            'password_confirm': 'Vuelve a escribir la contraseña',
        }
        
        for field_name, field in self.fields.items():
            if hasattr(field.widget, 'attrs'):
                placeholder_text = placeholders.get(field_name, '')
                field.widget.attrs.update({'placeholder': placeholder_text})

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo electrónico ya está registrado.")
        return email

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Las contraseñas no coinciden.")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

