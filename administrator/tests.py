from django.contrib.auth import get_user_model, authenticate
from django.test import TestCase

# Get the CustomUser model we defined in account/models.py
CustomUser = get_user_model()


class UserModelTests(TestCase):
    """Tests related to the CustomUser model and CustomUserManager."""

    def test_create_user_with_email(self):
        """Ensure a user can be created successfully with an email address."""
        email = 'voter@example.com'
        password = 'test-password123'
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name='Test',
            last_name='Voter'
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        # Check if the password was hashed correctly
        self.assertTrue(user.check_password(password))

    def test_create_superuser(self):
        """Ensure a superuser can be created with admin privileges."""
        email = 'admin@example.com'
        admin_user = CustomUser.objects.create_superuser(
            email=email,
            password='admin-password',
            first_name='Super',
            last_name='Admin'
        )
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_create_user_no_email_raises_error(self):
        """Ensure creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(email=None, password='test-password')


class AuthenticationTests(TestCase):
    """Tests related to the custom EmailBackend login."""

    def setUp(self):
        # Create a user to test authentication against
        self.email = 'test@login.com'
        self.password = 'secureP@ss1'
        CustomUser.objects.create_user(
            email=self.email,
            password=self.password,
            first_name='Login',
            last_name='Test'
        )

    def test_email_login_success(self):
        """Test authentication using the email and correct password."""
        user = authenticate(email=self.email, password=self.password)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.email)

    def test_email_login_failure(self):
        """Test authentication with an incorrect password fails."""
        user = authenticate(email=self.email, password='wrong-password')
        self.assertIsNone(user)
