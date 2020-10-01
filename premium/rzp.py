import razorpay
from decouple import config

client = razorpay.Client(auth=(config("RAZORPAY_API_KEY"), config("RAZORPAY_API_SECRET")))


def create_order(order_currency, order_amount, order_reciept, notes):
    instance = client.order.create({
        "amount": order_amount, 
        "currency":order_currency, 
        "receipt":order_reciept,
        "notes": notes
    })
    return instance


def get_all_orders():
    instance = client.order.all()
    return instance


def get_payments():
    instance = client.order.payments("order_FgvxlOQ1CQVBgv")
    return instance

def capture_payment():
    instance = client.payment.capture("pay_FgwKwl6nfY5f4Z", "150000", {"currency":"INR"})
    return instance

def fetch_payment():
    instance = client.payment.fetch('pay_FgwKwl6nfY5f4Z')
    return instance

# print(fetch_payment())