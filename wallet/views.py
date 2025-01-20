from django.conf import settings

from cart.models import Cart
from rest_framework.decorators import api_view
from django.http import JsonResponse

from course.models import UserCourse
from .models import Transaction
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Transaction, Payment
import requests
import json
import requests
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.conf import settings


@api_view(['POST'])
def start_payment(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()

    if not cart:
        return JsonResponse({"error": "سبد خرید یافت نشد"})

    # ایجاد تراکنش پرداخت
    amount = cart.total_amount()
    transaction = Transaction.objects.create(
        user=user,
        amount=amount,
        transaction_type='deposit',
        status='pending',
        message=f"پرداخت برای سبد خرید {user.user_name}"
    )

    # ایجاد پرداخت جدید
    payment = Payment.objects.create(
        user=user,
        cart=cart,
        transaction=transaction
    )

    # شروع پرداخت از طریق زرین‌پال
    try:
        payment_url = payment.initiate_payment()
        return JsonResponse({"payment_url": payment_url})
    except Exception as e:
        return JsonResponse({"error": str(e)})


@api_view(['GET'])
def verify_payment(request):
    status = request.GET.get("Status")
    authority = request.GET.get("Authority")
    # amount = request.GET.get("Amount")
    payment = Payment.objects.get(transaction__authority=authority)
    if status == "Ok":
        # ارسال درخواست تایید پرداخت از زرین‌پال
        url = "https://payment.zarinpal.com/pg/v4/payment/verify.json"
        data = {
            'merchant_id': settings.MERCHANT_ID,
            'amount': payment.cart.total_amount(),
            'authority': authority
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            if response_data['data']['code'] == 100:
                # تایید پرداخت موفق
                transaction = Transaction.objects.filter(authority=authority).first()
                if transaction:
                    transaction.status = 'success'
                    transaction.save()
                    # ثبت خرید کاربر
                    for i in payment.cart.items.all():
                        UserCourse.objects.create(
                            user=payment.user,
                            course=i.course,
                            transaction=transaction,
                            is_paid=True
                        )
                    # بروزرسانی وضعیت پرداخت
                    payment = Payment.objects.filter(transaction=transaction).first()
                    payment.status = 'completed'
                    payment.save()

                    return JsonResponse({"message": "پرداخت موفقیت‌آمیز بود"})
                else:
                    return JsonResponse({"error": "تراکنش یافت نشد"})
            else:
                return JsonResponse({"error": "پرداخت ناموفق بود"})
        else:
            return JsonResponse({"error": "خطا در ارتباط با زرین‌پال"})
    else:
        return JsonResponse({"error": "پرداخت ناموفق"})

@api_view(['POST'])
def get_payment_url(request):
    user = request.user
    cart_id = request.data.get('cart_id')

    cart = Cart.objects.filter(user=user, id=cart_id).first()

    if not cart:
        return JsonResponse({"error": "سبد خرید یافت نشد"}, status=404)

    total_amount = sum(item.course.price * item.quantity for item in cart.items.all())

    if total_amount <= 0:
        return JsonResponse({"error": "سبد خرید خالی است یا مبلغ پرداخت صحیح نیست."}, status=400)

    transaction = Transaction.objects.create(
        wallet=user.wallet,
        amount=total_amount,
        transaction_type='deposit',
        status='pending',
        message=f"پرداخت برای سبد خرید {cart_id}"
    )

    url = "https://api.zarinpal.com/pg/v4/payment/request.json"
    data = {
        'merchant_id': settings.MERCHANT_ID,
        'amount': total_amount,
        'callback_url': settings.CALLBACK_URL,
        'description': f"پرداخت برای سبد خرید {cart_id}"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        response_data = response.json()

        if response_data['data']['code'] == 100:
            authority = response_data['data']['authority']
            transaction.authority = authority
            transaction.save()

            payment_url = response_data['data']['url']
            return JsonResponse({"payment_url": payment_url})

        else:
            return JsonResponse({"error": response_data['data']['message']}, status=400)

    else:
        return JsonResponse({"error": "خطا در ارتباط با زرین‌پال"}, status=500)


@api_view(['GET'])
def get_transactions(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).values(
        'id', 'transaction_type', 'amount', 'status', 'timestamp', 'message', 'authority'
    )

    if not transactions:
        return JsonResponse({"error": "تراکنشی یافت نشد"}, status=404)

    return JsonResponse(list(transactions), safe=False)
