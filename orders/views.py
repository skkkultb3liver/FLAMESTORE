import datetime

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from products.forms import ReviewForm
from products.models import ReviewsRating
from .forms import *
from cart.models import CartItem
from .models import *


def payments(request):
    current_user = request.user

    order = Order.objects.filter(user=current_user).order_by('-id')[0]

    payment = Payment(
        user=request.user,
        payment_id=order.order_number,
        amount_paid=order.order_total,
        status=order.status,
    )

    payment.save()

    order.payment = payment
    order.ip_ordered = True
    order.status = 'Accepted'
    order.save()

    cart_items = CartItem.objects.filter(user=current_user)

    for item in cart_items:
        order_product = OrderProduct()

        order_product.order_id = order.id
        order_product.payment = payment
        order_product.user_id = request.user.id
        order_product.product_id = item.product_id
        order_product.qty = item.qty
        order_product.product_price = item.product.price
        order_product.ordered = True

        order_product.save()

        cart_item = CartItem.objects.get(id=item.id)

        product_variation = cart_item.variation.all()
        order_product = OrderProduct.objects.get(id=order_product.id)
        order_product.variation.set(product_variation)

        order_product.save()

        #REDUCE PRODUCT QTY AFTER ORDERING
        product = Product.objects.get(id=item.product_id)
        product.stock -= order_product.qty
        product.save()

    #CLEAR CART AFTER ORDERiNG
    CartItem.objects.filter(user=request.user).delete()

    #ORDER RECEIVED MAIL
    mail_subj = "Thank you for your order!"
    msg = render_to_string('orders/order_recieve.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subj, msg, to=[to_email])
    send_email.send()

    # ==========================================================

    data = {
        'order_number': order.order_number,
        'p_id': payment.payment_id,
    }

    return redirect(order_complete, order_number=order.order_number)


@require_http_methods(['POST'])
def place_order(request, total=0, qty=0):

    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('store')

    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.qty)
        qty += cart_item.qty

    tax = int((2 * total) // 100)
    grand_total = total + tax

    if request.method == 'POST':

        form = OrderForm(request.POST)
        print(f'request: {request.method}')

        if form.is_valid():
            print('form is valid')
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            country = form.cleaned_data['country']
            city = form.cleaned_data['city']
            address_line_1 = form.cleaned_data['address_line_1']
            address_line_2 = form.cleaned_data['address_line_2']

            order_total = grand_total
            tax = tax

            ip = request.META.get('REMOTE_ADDR')

            data = Order.objects.create(
                user=current_user,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                country=country,
                city=city,
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                order_total=order_total,
                tax=tax,
                ip=ip,
            )

            print(f"data = {data}")
            data.save()
            print(f"Order object with id {data.id} was created.")

            #GENERATE ORDER NUMBER
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)

            cur_date = d.strftime("%Y%m%d")
            order_number = cur_date + str(data.id)
            data.order_number = order_number

            data.save()

            order = Order.objects.get(user=current_user, ip_ordered=False, order_number=order_number)

            context = {
                'order': order,
                'cart_items': cart_items,
                'grand_total': order_total,
                'tax': tax,
                'total': total,

            }
            return render(request, 'orders/payments.html', context)
        else:
            print(form.errors)

    return render(request, 'products/checkout.html')


def order_complete(request, order_number):

    try:
        order = Order.objects.filter(user=request.user, ip_ordered=True, order_number=order_number).order_by('-id')[0]
        products = OrderProduct.objects.filter(user=request.user, order=order)

        subtotal = 0

        for i in products:
            subtotal += i.product.price * i.qty

        context = {
            'order': order,
            'products': products,
            'subtotal': subtotal,
        }

        return render(request, 'orders/order_complete.html', context)

    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('store')

