from django import forms
from .models import Account, Category, Transaction


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'account_type', 'starting_balance']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g. Main Checking'
            }),
            'starting_balance': forms.NumberInput(attrs={
                'placeholder': '0.00'
            }),
        }