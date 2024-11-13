# scraper/forms.py
from django import forms

class CaseForm(forms.Form):
    case_number = forms.CharField(
        label="Número de Radicado",
        max_length=23,
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese los 23 dígitos del número de Radicación'})
    )
