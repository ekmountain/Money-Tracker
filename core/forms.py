from django import forms
from .models import Account, Category, Transaction
from django.db import models
from .models import Account, Category, Transaction, Budget


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
            
class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month', 'year']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'placeholder': '0.00'
            }),
            'month': forms.NumberInput(attrs={
                'min': 1,
                'max': 12,
                'placeholder': 'e.g. 6 for June'
            }),
            'year': forms.NumberInput(attrs={
                'min': 2000,
                'max': 2100,
                'placeholder': 'e.g. 2026'
            }),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(
                models.Q(user=user) | models.Q(user=None),
                category_type='expense'
            )