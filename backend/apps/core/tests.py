"""
Tests for Core app
"""
from django.test import TestCase
from apps.core.models import Company, User


class CompanyModelTest(TestCase):
    """Tests for Company model"""

    def setUp(self):
        self.company = Company.objects.create(
            name='ICTSI Brasil',
            company_type='ICTSI',
            is_active=True
        )

    def test_company_creation(self):
        """Test company was created correctly"""
        self.assertEqual(self.company.name, 'ICTSI Brasil')
        self.assertEqual(self.company.company_type, 'ICTSI')
        self.assertTrue(self.company.is_active)

    def test_company_str(self):
        """Test company string representation"""
        self.assertEqual(str(self.company), 'ICTSI Brasil (ICTSI)')


class UserModelTest(TestCase):
    """Tests for User model"""

    def setUp(self):
        self.company = Company.objects.create(
            name='ICTSI Brasil',
            company_type='ICTSI',
            is_active=True
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            company=self.company,
            role='INSPECTOR'
        )

    def test_user_creation(self):
        """Test user was created correctly"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.company, self.company)
        self.assertEqual(self.user.role, 'INSPECTOR')

    def test_user_full_name(self):
        """Test user full name property"""
        self.user.first_name = 'Test'
        self.user.last_name = 'User'
        self.user.save()
        self.assertEqual(self.user.full_name, 'Test User')
