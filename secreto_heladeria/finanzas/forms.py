from django import forms
from django.forms.models import BaseInlineFormSet
from .models import Transaccion
from django.core.exceptions import ValidationError

class TransaccionInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        for form in self.forms:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                monto = form.cleaned_data.get('monto')
                if monto is not None and monto <= 0:
                    raise ValidationError("El monto de cada transacción debe ser mayor a 0.")
