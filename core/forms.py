from django import forms
from .models import Account, Category, Transaction
from django.db import models


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
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'category_type']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g. Side Income'
            }),
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'category', 'amount', 'transaction_type', 'date', 'memo']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date'
            }),
            'memo': forms.TextInput(attrs={
                'placeholder': 'Optional note'
            }),
            'amount': forms.NumberInput(attrs={
                'placeholder': '0.00'
            }),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['account'].queryset = Account.objects.filter(user=user)
            self.fields['category'].queryset = Category.objects.filter(
                models.Q(user=user) | models.Q(user=None)
            )