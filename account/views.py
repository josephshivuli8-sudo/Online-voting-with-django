from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import CustomUserForm
from django.contrib.auth import authenticate, login
from voting.forms import VoterForm

def account_login(request):
    # 🔥 CLEAR ANY OLD MESSAGES
    storage = messages.get_messages(request)
    storage.used = True

    if request.user.is_authenticated:
        if request.user.user_type == '1':
            return redirect("adminDashboard")
        return redirect("voterDashboard")

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect(
                "adminDashboard" if user.user_type == '1' else "voterDashboard"
            )

        messages.error(request, "Invalid login details")

    return render(request, "voting/login.html")


def account_register(request):
    userForm = CustomUserForm(request.POST or None)
    voterForm = VoterForm(request.POST or None)

    context = {
        'form1': userForm,
        'form2': voterForm
    }

    if request.method == 'POST':
        if userForm.is_valid() and voterForm.is_valid():
            user = userForm.save(commit=False)
            voter = voterForm.save(commit=False)

            user.save()
            voter.admin = user
            voter.save()

            messages.success(request, "Account created successfully. You can now login.")
            return redirect(reverse('account_login'))
        else:
            messages.error(request, "Provided data failed validation")

    return render(request, "voting/reg.html", context)

def account_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "You have been logged out successfully")
    else:
        messages.error(request, "You need to be logged in to perform this action")

    return redirect(reverse("account_login"))


