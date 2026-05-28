from django.db import models
from django.contrib.auth.models import User

# 3 main models: Account, Category, Transaction
class Account(models.Model):
    ACCOUNT_TYPES = [
        ('checking', 'Checking'),
        ('savings', 'Savings'),
        ('credit', 'Credit Card'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    starting_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_account_type_display()})"

    def get_balance(self):
        from .models import Transaction
        income = self.transactions.filter(
            transaction_type='income').aggregate(
            total=models.Sum('amount'))['total'] or 0
        expenses = self.transactions.filter(
            transaction_type='expense').aggregate(
            total=models.Sum('amount'))['total'] or 0
        return self.starting_balance + income - expenses

    class Meta:
        ordering = ['name']
    
class Category(models.Model):
    CATEGORY_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"

    @property
    def is_default(self):
        return self.user is None

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'
        
class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('transfer', 'Transfer'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    date = models.DateField()
    memo = models.CharField(max_length=255, blank=True)
    transfer_id = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.transaction_type} - ${self.amount}"

    class Meta:
        ordering = ['-date']