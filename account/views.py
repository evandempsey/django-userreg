from datetime import datetime

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import RequestContext

from models import ActivationKey, RecoveryKey, DeactivationKey
from forms import RegistrationForm, ChangePasswordForm, RecoveryForm, DeactivationForm, ResetPasswordForm
from accountemailmanager import AccountEmailManager as EmailManager
from settings import SITE_URL, LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL


def authenticateUser(request):
    """
    Authenticate the user
    """
    params = {"errors": []}

    if request.method == "POST":
        # Credentials are being submitted
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])

        if user is not None:
            if user.is_active:
                # Login successful
                login(request, user)
                return HttpResponseRedirect(LOGIN_REDIRECT_URL)

        params["errors"].append("Incorrect username and password.")

    return render_to_response("account/login.html",
                              params,
                              context_instance=RequestContext(request))


def deauthenticateUser(request):
    """
    Log out the user.
    """
    logout(request)
    return HttpResponseRedirect(LOGOUT_REDIRECT_URL)


@login_required
def password(request):
    """
    Change the user's password.
    """
    # If there is POST data, try to validate and use it
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)

        # If new password is valid, change it and show "changed" page.
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data["password1"])
            user.save()
            return render_to_response("account/password_changed.html",
                                      context_instance=RequestContext(request))

    # If there is no POST data, send empty form
    else:
        form = ChangePasswordForm()

    params = {"form": form}
    return render_to_response("account/change_password.html",
                              params,
                              context_instance=RequestContext(request))


def register(request):
    """
    Register a new user.
    """
    # User info is being submitted
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        params = {"form": form}

        if form.is_valid():
            # Create user
            user = User.objects.create_user(form.cleaned_data["username"],
                                            form.cleaned_data["email"],
                                            form.cleaned_data["password1"])
            user.is_active = False
            user.save()

            # Send activation email
            emailManager = EmailManager(user)
            activationEmail = emailManager.activationEmail()
            activationEmail.send()

            return render_to_response("account/registration_complete.html",
                                      {},
                                      context_instance=RequestContext(request))

    # If there is no POST data, send blank registration form.
    else:
        params = {"form": RegistrationForm()}

    return render_to_response("account/register.html",
                              params,
                              context_instance=RequestContext(request))


def requestRecovery(request):
    """
    Accept email address from user and send recovery email.
    """
    if request.method == "POST":
        form = RecoveryForm(request.POST)
        params = {"form": form}

        if form.is_valid():
            # Send recovery email.
            user = User.objects.get(email=form.cleaned_data["email"])
            emailManager = EmailManager(user)
            recoveryEmail = emailManager.recoveryEmail()
            recoveryEmail.send()
            return render_to_response("account/recovery_email_sent.html",
                                      context_instance=RequestContext(request))

    # Send blank form if no POST data present.
    else:
        form = RecoveryForm()
        params = {"form": form}

    return render_to_response("account/recover_account.html",
                              params,
                              context_instance=RequestContext(request))


def recover(request, username, key):
    """
    Recover an account.
    """
    # Check if the username belongs to a real user.
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponseRedirect(SITE_URL)

    # Check if that user has an unused, unexpired recovery key.
    try:
        recoveryKey = RecoveryKey.objects.get(user=user,
                                              key=key,
                                              used=False,
                                              expires__gte=datetime.today())
    except RecoveryKey.DoesNotExist:
        return HttpResponseRedirect(SITE_URL)

    # If we got this far, things are good so deal with the password change.
    # If there is POST data, try to process it
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)

        # If new password is valid, change it and redirect to "changed" page.
        # Also record that the key has been used.
        if form.is_valid():
            user.set_password(form.cleaned_data["password1"])
            user.save()
            recoveryKey.used = True
            recoveryKey.save()
            return render_to_response("account/password_reset.html",
                                      context_instance=RequestContext(request))
    else:
        form = ResetPasswordForm()

    params = {"form": form,
              "username": username,
              "key": key}
    return render_to_response("account/reset_password.html",
                              params,
                              context_instance=RequestContext(request))


def activate(request, username, key):
    """
    Activate a new account.
    """
    # Get the user account associated wth the username.
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponseRedirect(SITE_URL)

    # Check for a good activation key.
    try:
        key = ActivationKey.objects.get(user=user,
                                        key=key,
                                        used=False,
                                        expires__gte=datetime.today())
    except ActivationKey.DoesNotExist:
        return HttpResponseRedirect(SITE_URL)

    # If we got this far, activate the account.
    user.is_active = True
    user.save()

    # Record that the activation key has been used.
    key.used = True
    key.save()

    # Tell the motherfucking user. They dig that.
    return render_to_response("account/account_activated.html",
                              context_instance=RequestContext(request))


@login_required
def requestDeactivation(request):
    """
    Prompt user for credentials and send deactivation email.
    """
    if request.method == "POST":
        form = DeactivationForm(request.POST)

        if form.is_valid() \
                and request.user.username == form.cleaned_data["username"]:
            # Send deactivation email
            user = User.objects.get(username=form.cleaned_data["username"])
            emailManager = EmailManager(user)
            deactivationEmail = emailManager.deactivationEmail()
            deactivationEmail.send()

            return render_to_response("account/deactivation_email_sent.html",
                                      context_instance=RequestContext(request))

    else:
        form = DeactivationForm()

    params = {"form": form}
    return render_to_response("account/deactivate_account.html",
                              params,
                              context_instance=RequestContext(request))


def deactivate(request, username=None, key=None):
    """
    Deactivate an account.
    """

    # First check if that user exists.
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponseRedirect(SITE_URL)

    # Get activation key for that user.
    try:
        key = DeactivationKey.objects.get(user=user,
                                          key=key,
                                          used=False,
                                          expires__gte=datetime.today())
    except DeactivationKey.DoesNotExist:
        return HttpResponseRedirect(SITE_URL)

    # If we got this far, the key is valid. Deactivate account
    # and set the used field on the key to True.
    user.is_active = False
    user.save()
    key.used = True
    key.save()

    # If the user is logged in, log him out.
    logout(request)

    # Tell the user the account has been deactivated.
    return render_to_response("account/account_deactivated.html",
                              context_instance=RequestContext(request))


@login_required
def manageAccount(request):
    """
    Account management page.
    """
    return render_to_response("account/manage.html",
                              context_instance=RequestContext(request))
