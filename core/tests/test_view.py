from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


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