from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib import messages, auth

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


            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password, )
            user.phone_number = phone_number

            user.save()
            messages.success(request, 'Registration successful!')

            return redirect('register')

    else:
        form = RegisterForm()

    context = {
        'form': form,
    }

    return render(request, "accounts/reg-screen.html", context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        print(email, password)

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('store')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, "accounts/login.html")


@login_required(login_url='login')
def logout(request):
    auth.logout(request)

    messages.success(request, "You're logged out.")

    return redirect('login')