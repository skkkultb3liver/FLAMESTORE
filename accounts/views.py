from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage

from cart.models import Cart, CartItem
from cart.views import _cart_id
from orders.models import Order
from .forms import RegisterForm
from django.contrib import messages, auth

from django.utils.http import urlencode

# Create your views here.
from .models import Account
import requests
import urlparse3


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

            return redirect(f"/accounts/register/?command=verification&email={email}")

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

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()

                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    product_variation_list = []

                    for item in cart_item:
                        var = item.variation.all()
                        product_variation_list.append(list(var))

                    cart_item = CartItem.objects.filter(user=user)
                    ex_vars_list = []
                    id_item_list = []

                    for item in cart_item:
                        ex_variation = item.variation.all()
                        ex_vars_list.append(list(ex_variation))
                        id_item_list.append(item.id)

                    for p in product_variation_list:
                        if p in ex_vars_list:
                            ind = ex_vars_list.index(p)
                            item_id = id_item_list[ind]

                            item = CartItem.objects.get(id=item_id)
                            item.qty += 1
                            item.user = user
                            item.save()

                        else:
                            cart_item = CartItem.objects.filter(cart=cart)

                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass

            auth.login(request, user)
            messages.success(request, "You're now logged in!")

            url = request.META.get('HTTP_REFERER')

            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                print(params)
                if 'next' in params:
                    next_page = params['next']
                    print(next_page)
                    return redirect(next_page)

            except:
                return redirect('profile')

        else:
            messages.error(request, "Invalid login credentials.")
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
        messages.error(request, 'Invalid activation link.')

        return redirect('register')


@login_required(login_url='login')
def profile(request):

    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, ip_ordered=True)
    orders_count = orders.count()

    context = {
        'orders_count': orders_count
    }

    return render(request, 'accounts/profile-info.html', context)


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            mail_subj = "Reset your password"
            msg = render_to_string('accounts/reset_password_alert.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subj, msg, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset has sent to your email address.')
            return redirect('login')

        else:
            messages.error(request, 'Account with such an email does not exist.')
            return redirect('forgot_password')

    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password.')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired.')
        return redirect('login')


def reset_password(request):

    if request.method == 'POST':
        password = request.POST['new_password']
        c_password = request.POST['confirm_password']

        if password == c_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password was successfully changed!')
            return redirect('login')
        else:
            messages.error(request, 'Passwords dont match.')
            return redirect('reset_password')

    else:
        return render(request, 'accounts/reset_password.html')


# PROFILE SETTINGS


def my_orders(request):

    orders = Order.objects.filter(user=request.user, ip_ordered=True).order_by('-created_at')

    context = {
        'orders': orders,
    }
    return render(request, 'accounts/user_profile/my_orders.html', context)