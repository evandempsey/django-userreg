from django.test import TestCase
from django.contrib.auth.models import User


class AuthenticationTestCase(TestCase):
    """
    Tests the ability to log in and out.
    """

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.user.save()

    def test_login_successful(self):
        """
        It is possible to log in with the right credentials.
        """
        post_data = {"username": "testuser",
                     "password": "password"}
        response = self.client.post("/account/login/", post_data)

        # The user should have been redirected after a successful login.
        self.assertEquals(response.status_code, 302)

    def test_login_unsuccessful(self):
        """
        It is not possible to log in with the wrong credentials.
        """
        post_data = {"username": "testuser",
                     "password": "wrongpassword"}
        response = self.client.post("/account/login/", post_data)

        # The user should be shown the same page with errors after
        # an unsuccessful login attempt.
        self.assertEquals(response.status_code, 200)

    def test_user_does_not_exist(self):
        """
        It is not possible to log in if the user does not exist.
        """
        post_data = {"username": "fakeuser",
                     "password": "password"}
        response = self.client.post("/account/login/", post_data)

        # The user should have been redirected after a successful login.
        self.assertEquals(response.status_code, 200)

    def tearDown(self):
        self.user.delete()


class ChangePasswordTestCase(TestCase):
    """
    Tests the ability for users to change their passwords.
    """

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.user.save()

    def test_unauthenticated(self):
        """
        The page is not accessible if the user is not logged in.
        """
        response = self.client.get("/account/manage/password/")
        self.assertEquals(response.status_code, 302)

    def test_authenticated(self):
        """
        The page is accessible if the user is logged in.
        """
        login = self.client.login(username="testuser", password="password")
        self.assertTrue(login)

        response = self.client.get("/account/manage/password/")
        self.assertEquals(response.status_code, 200)

    def test_wrong_credentials(self):
        """
        It is not possible to change the password when
        the wrong original credentials are provided.
        """
        login = self.client.login(username="testuser", password="password")
        self.assertTrue(login)

        post_data = {"username": "testuser",
                     "password": "wrongpassword",
                     "new_password": "newpassword",
                     "confirm_password": "newpassword"}

        response = self.client.post("/account/manage/password/", post_data)
        self.assertEquals(response.status_code, 200)

        login = self.client.login(username="testuser", password="newpassword")
        self.assertFalse(login)

    def test_change_password_matching_passwords(self):
        """
        It is possible to change passwords when matching new passwords are given.
        """
        login = self.client.login(username="testuser", password="password")
        self.assertTrue(login)

        post_data = {"username": "testuser",
                     "password": "password",
                     "new_password": "newpassword",
                     "confirm_password": "newpassword"}

        response = self.client.post("/account/manage/password/", post_data)
        self.assertEquals(response.status_code, 200)

        login = self.client.login(username="testuser", password="newpassword")
        self.assertTrue(login)

    def test_change_password_not_matching_passwords(self):
        """
        It is not possible to change passwords when non-matching new passwords are given.
        """
        login = self.client.login(username="testuser", password="password")
        self.assertTrue(login)

        post_data = {"username": "testuser",
                     "password": "password",
                     "new_password": "newpassword",
                     "confirm_password": "differentnewpassword"}

        response = self.client.post("/account/manage/password/", post_data)
        self.assertEquals(response.status_code, 200)

        login = self.client.login(username="testuser", password="newpassword")
        self.assertFalse(login)

    def tearDown(self):
        self.user.delete()


class RegistrationTestCase(TestCase):
    """
    Tests the ability for new users to register.
    """

    def setUp(self):
        self.user = User.objects.create_user("testuser", "test@test.com", "password")
        self.user.save()

    def test_registration_form(self):
        """
        Test that the registration form loads in the first place.
        """
        response = self.client.get("/account/register/")
        self.assertEquals(response.status_code, 200)

