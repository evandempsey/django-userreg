from django.test import TestCase


class AccountTest(TestCase):
    """
    Test cases for django views.
    """

    def testLoginPage(self):
        """
        Test that the login page can be loaded.
        """
        response = self.client.get("/account/login/")
        self.assertEqual(response.status_code, 200)

    def testRegistrationPage(self):
        """
        Test that the registration page can be loaded.
        """
        response = self.client.get("/account/register/")
        self.assertEqual(response.status_code, 200)

    def testRecoveryPage(self):
        """
        Test that the registration page can be loaded.
        """
        response = self.client.get("/account/recover/")
        self.assertEqual(response.status_code, 200)
