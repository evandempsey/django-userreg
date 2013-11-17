from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


class DeactivationForm(forms.Form):
    """
    Account deactivation form.
    """
    username = forms.CharField(max_length=30, label="Username")
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")

    def clean(self):
        """
        Check the user's credentials.
        """
        username = self.cleaned_data.get("username", None)
        password = self.cleaned_data.get("password", None)

        user = authenticate(username=username,
                            password=password)

        if user is None:
            raise forms.ValidationError("Incorrect username and password.")
        else:
            return self.cleaned_data


class RecoveryForm(forms.Form):
    """
    Account recovery form.
    """
    email = forms.EmailField()

    def clean_email(self):
        """
        Make sure the email address is associated with an account.
        """
        error_string = "There is no account associated with that email address."
        email = self.cleaned_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(error_string)

        return email


class ResetPasswordForm(forms.Form):
    """
    Reset a password after clicking link in recovery email.
    """
    new_password = forms.CharField(widget=forms.PasswordInput(), min_length=5, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), min_length=5, label="Confirm Password")

    def clean(self):
        """
        Make sure that the new passwords match.
        """
        new_password = self.cleaned_data.get("new_password", None)
        confirm_password = self.cleaned_data.get("confirm_password", None)
        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return self.cleaned_data


class ChangePasswordForm(forms.Form):
    """
    Change the password on an account.
    """
    username = forms.CharField(max_length=30, label="Username")
    password = forms.CharField(widget=forms.PasswordInput(), min_length=5, label="Password")
    new_password = forms.CharField(widget=forms.PasswordInput(), min_length=5, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), min_length=5, label="Confirm Password")

    def clean(self):
        """
        Make sure supplied credentials are valid
        and that new passwords match.
        """
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username,
                            password=password)
        if user is None:
            raise forms.ValidationError("Incorrect username and password.")

        new_password = self.cleaned_data.get("new_password", None)
        confirm_password = self.cleaned_data.get("confirm_password", None)
        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return self.cleaned_data


class RegistrationForm(forms.Form):
    """
    Register a new user.
    """
    username = forms.CharField(max_length=30, min_length=4, label="Username")
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput(), min_length=5, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(), min_length=5, label="Confirm Password")

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise forms.ValidationError(
            "Username %s is already taken." % username)

    def clean(self):
        """
        Make sure that the two passwords match.
        """
        password = self.cleaned_data.get("password", None)
        confirm_password = self.cleaned_data.get("confirm_password", None)

        if password == confirm_password:
            return self.cleaned_data

        raise forms.ValidationError("Passwords do not match.")
