from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# These tests cover the core views of the application, including authentication, account management, and transaction management. Each test checks that the appropriate status codes are returned and that the expected changes occur in the database when creating, editing, or deleting accounts and transactions. Additional tests can be added to cover edge cases and other functionality as needed.
class AuthTests(TestCase):
    # Set up a test user for authentication tests

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123'
        )

    def test_register_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_dashboard_redirects_when_logged_out(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_loads_when_logged_in(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_user_can_register(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@test.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

# Additional tests for login, logout, and other authentication-related functionality can be added here.
from core.models import Account
from decimal import Decimal


class AccountViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser2',
            password='testpass123'
        )
        self.client.login(username='testuser2', password='testpass123')
        self.account = Account.objects.create(
            user=self.user,
            name='Test Checking',
            account_type='checking',
            starting_balance=Decimal('1000.00')
        )

    def test_account_list_loads(self):
        response = self.client.get(reverse('account_list'))
        self.assertEqual(response.status_code, 200)

    def test_account_list_redirects_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('account_list'))
        self.assertEqual(response.status_code, 302)

    def test_account_create(self):
        response = self.client.post(reverse('account_create'), {
            'name': 'New Savings',
            'account_type': 'savings',
            'starting_balance': '500.00'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Account.objects.filter(name='New Savings').exists())

    def test_account_edit(self):
        response = self.client.post(
            reverse('account_edit', args=[self.account.pk]), {
                'name': 'Updated Checking',
                'account_type': 'checking',
                'starting_balance': '2000.00'
            })
        self.assertEqual(response.status_code, 302)
        self.account.refresh_from_db()
        self.assertEqual(self.account.name, 'Updated Checking')

    def test_account_delete(self):
        response = self.client.post(
            reverse('account_delete', args=[self.account.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Account.objects.filter(pk=self.account.pk).exists())

# Transaction tests will be added here once the transaction views are implemented.
from core.models import Account, Category, Transaction
import datetime


class TransactionViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser3',
            password='testpass123'
        )
        self.client.login(username='testuser3', password='testpass123')
        self.account = Account.objects.create(
            user=self.user,
            name='Test Checking',
            account_type='checking',
            starting_balance=Decimal('1000.00')
        )
        self.category = Category.objects.create(
            name='Test Category',
            category_type='expense'
        )

    def test_transaction_list_loads(self):
        response = self.client.get(reverse('transaction_list'))
        self.assertEqual(response.status_code, 200)

    def test_transaction_list_redirects_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('transaction_list'))
        self.assertEqual(response.status_code, 302)

    def test_transaction_create(self):
        response = self.client.post(reverse('transaction_create'), {
            'account': self.account.pk,
            'category': self.category.pk,
            'amount': '50.00',
            'transaction_type': 'expense',
            'date': datetime.date.today(),
            'memo': 'Test transaction'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Transaction.objects.filter(memo='Test transaction').exists())

    def test_transaction_edit(self):
        transaction = Transaction.objects.create(
            account=self.account,
            category=self.category,
            amount=Decimal('50.00'),
            transaction_type='expense',
            date=datetime.date.today(),
            memo='Original memo'
        )
        response = self.client.post(
            reverse('transaction_edit', args=[transaction.pk]), {
                'account': self.account.pk,
                'category': self.category.pk,
                'amount': '75.00',
                'transaction_type': 'expense',
                'date': datetime.date.today(),
                'memo': 'Updated memo'
            })
        self.assertEqual(response.status_code, 302)
        transaction.refresh_from_db()
        self.assertEqual(transaction.memo, 'Updated memo')

    def test_transaction_delete(self):
        transaction = Transaction.objects.create(
            account=self.account,
            category=self.category,
            amount=Decimal('50.00'),
            transaction_type='expense',
            date=datetime.date.today(),
            memo='To be deleted'
        )
        response = self.client.post(
            reverse('transaction_delete', args=[transaction.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Transaction.objects.filter(pk=transaction.pk).exists())

    def test_transaction_affects_balance(self):
        Transaction.objects.create(
            account=self.account,
            category=self.category,
            amount=Decimal('200.00'),
            transaction_type='expense',
            date=datetime.date.today()
        )
        self.assertEqual(self.account.get_balance(), Decimal('800.00'))