import stripe
from config import settings

stripe.api_key = settings.STRIPE_API

def create_stripe_product(product):
    stripe_product = stripe.Product.create(name=product.name)
    return stripe_product

def create_stripe_price(amount, product):
    stripe_price = stripe.Price.create(
        currency="rub",
        unit_amount=int(amount) * 100,
        product_data={"name": product.get("id")},
    )
    return stripe_price

def create_srtipe_session(session):
    stripe_session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": session.get("id"), "quantity": 1}],
        mode="payment",
    )
    id = stripe_session.get("id")
    url = stripe_session.get("url")
    status = stripe_session.get("status")
    return id, url, status