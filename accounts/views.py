from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage

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

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password,
            )
            user.phone_number = phone_number

            user.save()

            # ACTIVATION
            current_site = get_current_site(request)
            mail_subj = "Account activation"
            msg = render_to_string('accounts/email_verify.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subj, msg, to=[to_email])
            send_email.send()

            # messages.success(request, f'An email was sent to {to_email} to activate your account.')

            return redirect(f'/accounts/register/?command=verification&email={email}')

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


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account is activated!')

        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')

        return redirect('register')