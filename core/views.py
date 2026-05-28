from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Account, Category, Transaction
from .forms import AccountForm, TransactionForm, CategoryForm

# UserCreattionForm is a built-in Django form for user registration. Adding email field 
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user)
    return render(request, 'accounts/account_list.html', {'accounts': accounts})


@login_required
def account_create(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.success(request, 'Account created successfully!')
            return redirect('account_list')
    else:
        form = AccountForm()
    return render(request, 'accounts/account_create.html', {'form': form})


@login_required
def account_edit(request, pk):
    account = Account.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account updated successfully!')
            return redirect('account_list')
    else:
        form = AccountForm(instance=account)
    return render(request, 'accounts/account_edit.html', {'form': form, 'account': account})


@login_required
def account_delete(request, pk):
    account = Account.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        account.delete()
        messages.success(request, 'Account deleted successfully!')
        return redirect('account_list')
    return render(request, 'accounts/account_delete.html', {'account': account})

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(
        account__user=request.user
    ).select_related('account', 'category')
    return render(request, 'transactions/transaction_list.html', 
        {'transactions': transactions})


@login_required
def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.user, request.POST)
        if form.is_valid():
            transaction = form.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('transaction_list')
    else:
        form = TransactionForm(user=request.user)
    return render(request, 'transactions/transaction_create.html', {'form': form})


@login_required
def transaction_edit(request, pk):
    transaction = Transaction.objects.get(pk=pk, account__user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.user, request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully!')
            return redirect('transaction_list')
    else:
        form = TransactionForm(user=request.user, instance=transaction)
    return render(request, 'transactions/transaction_edit.html', 
        {'form': form, 'transaction': transaction})


@login_required
def transaction_delete(request, pk):
    transaction = Transaction.objects.get(pk=pk, account__user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('transaction_list')
    return render(request, 'transactions/transaction_delete.html', 
        {'transaction': transaction})