from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Account, Category, Transaction
from .forms import AccountForm, TransactionForm, CategoryForm
from django.shortcuts import get_object_or_404
from .models import Account, Category, Transaction, Budget
from .forms import AccountForm, TransactionForm, CategoryForm, BudgetForm

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
    account = get_object_or_404(Account, pk=pk, user=request.user)
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
    account = get_object_or_404(Account, pk=pk, user=request.user)
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
    transaction = get_object_or_404(Transaction, pk=pk, account__user=request.user)
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
    transaction = get_object_or_404(Transaction, pk=pk, account__user=request.user)
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted successfully!')
        return redirect('transaction_list')
    return render(request, 'transactions/transaction_delete.html', 
        {'transaction': transaction})

# category_list separates default and custom categories so they can be displayed separately in the template
@login_required
def category_list(request):
    default_categories = Category.objects.filter(user=None)
    custom_categories = Category.objects.filter(user=request.user)
    return render(request, 'categories/category_list.html', {
        'default_categories': default_categories,
        'custom_categories': custom_categories
    })


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category created successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'categories/category_create.html', {'form': form})


#category_edit and category_delete filter by user=request.user so users can only edit or delete their own custom categories, not the defaults
@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/category_edit.html', {
        'form': form,
        'category': category
    })


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    return render(request, 'categories/category_delete.html', {'category': category})

@login_required
def budget_list(request):
    budgets = Budget.objects.filter(user=request.user).select_related('category')
    return render(request, 'budgets/budget_list.html', {'budgets': budgets})


@login_required
def budget_create(request):
    if request.method == 'POST':
        form = BudgetForm(request.user, request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, 'Budget created successfully!')
            return redirect('budget_list')
    else:
        form = BudgetForm(user=request.user)
    return render(request, 'budgets/budget_create.html', {'form': form})


@login_required
def budget_edit(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.user, request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget updated successfully!')
            return redirect('budget_list')
    else:
        form = BudgetForm(user=request.user, instance=budget)
    return render(request, 'budgets/budget_edit.html', {
        'form': form,
        'budget': budget
    })


@login_required
def budget_delete(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Budget deleted successfully!')
        return redirect('budget_list')
    return render(request, 'budgets/budget_delete.html', {'budget': budget})