from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Account, Category, Transaction
from decimal import Decimal
import datetime


class AccountModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.account = Account.objects.create(
            user=self.user,
            name='Test Checking',
            account_type='checking',
            starting_balance=Decimal('1000.00')
        )

    def test_account_str(self):
        self.assertEqual(str(self.account), 'Test Checking (Checking)')

    def test_account_balance_with_no_transactions(self):
        self.assertEqual(self.account.get_balance(), Decimal('1000.00'))

    def test_account_balance_with_income(self):
        Transaction.objects.create(
            account=self.account,
            amount=Decimal('500.00'),
            transaction_type='income',
            date=datetime.date.today()
        )
        self.assertEqual(self.account.get_balance(), Decimal('1500.00'))

    def test_account_balance_with_expense(self):
        Transaction.objects.create(
            account=self.account,
            amount=Decimal('200.00'),
            transaction_type='expense',
            date=datetime.date.today()
        )
        self.assertEqual(self.account.get_balance(), Decimal('800.00'))


class CategoryModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.default_category = Category.objects.create(
            name='Groceries',
            category_type='expense'
        )
        self.custom_category = Category.objects.create(
            user=self.user,
            name='Side Income',
            category_type='income'
        )

    def test_default_category_str(self):
        self.assertEqual(str(self.default_category), 'Groceries (Expense)')

    def test_custom_category_str(self):
        self.assertEqual(str(self.custom_category), 'Side Income (Income)')

    def test_is_default_true(self):
        self.assertTrue(self.default_category.is_default)

    def test_is_default_false(self):
        self.assertFalse(self.custom_category.is_default)