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

    STATUS_CHOICES = [
        ('uncleared', 'Uncleared'),
        ('cleared', 'Cleared'),
        ('reconciled', 'Reconciled'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uncleared')
    date = models.DateField()
    memo = models.CharField(max_length=255, blank=True)
    transfer_id = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.transaction_type} - ${self.amount}"

    class Meta:
        ordering = ['-date']

class Reconciliation(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='reconciliations')
    opening_balance = models.DecimalField(max_digits=10, decimal_places=2)
    closing_balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.account.name} - {self.created_at.strftime('%B %Y')}"

    def get_cleared_balance(self):
        from django.db.models import Sum
        cleared = Transaction.objects.filter(
            account=self.account,
            status='cleared'
        ).aggregate(total=Sum('amount'))['total'] or 0
        return self.opening_balance + cleared

    def is_balanced(self):
        return self.get_cleared_balance() == self.closing_balance

    class Meta:
        ordering = ['-created_at']

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField()
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} - {self.month}/{self.year} (${self.amount})"

    # get_spent()calculates how much has been spent in that category for that month dynamically
    def get_spent(self):
        from django.db.models import Sum
        spent = Transaction.objects.filter(
            account__user=self.user,
            category=self.category,
            transaction_type='expense',
            date__month=self.month,
            date__year=self.year
        ).aggregate(total=Sum('amount'))['total'] or 0
        return spent
    
    # get_remaining() shows how much budget is left
    def get_remaining(self):
        return self.amount - self.get_spent()

    # get_percentage() returns a 0-100 value useful for progress bars in the template
    # min(..., 100) caps at 100% even if overspent
    def get_percentage(self):
        if self.amount == 0:
            return 0
        return min(int((self.get_spent() / self.amount) * 100), 100)

    class Meta:
        ordering = ['year', 'month']
        # unique_together prevents duplicate budgets for the same category and month        
        unique_together = ['user', 'category', 'month', 'year']