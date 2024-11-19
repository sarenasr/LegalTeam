from django import forms

class SubscriptionForm(forms.Form):
    email = forms.EmailField(label="Email")
    case_number = forms.CharField(
        label="Número de Radicado",
        max_length=23,
        widget=forms.TextInput(attrs={'placeholder': 'Ingrese los 23 dígitos del número de Radicación'})
    )