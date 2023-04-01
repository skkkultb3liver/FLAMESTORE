from django.shortcuts import render
from .forms import RegisterForm

# Create your views here.
from .models import Account


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number

            user.save()
    else:
        form = RegisterForm()

    comtext = {
        'form': form,
    }
    return render(request, "accounts/reg-screen.html", comtext)


def login(request):
    return render(request, "accounts/login.html")


def logout(request):
    return