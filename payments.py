"""
Gestion des paiements Stripe
"""
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
if not stripe.api_key:
    raise RuntimeError("STRIPE_SECRET_KEY is not set")
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET', 'whsec_...')


def create_checkout_session(*, order, base_url):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": order["pricing"]["currency"],   # 'eur'
                    "product_data": {
                        "name": order["label"]
                    },
                    "unit_amount": order["pricing"]["amount_total"],  # 69000
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=f"{base_url}/paiement/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{base_url}/commander/confirmation",
            locale="fr",
            metadata=order.get("metadata", {})
        )
        return session.url

    except Exception as e:
        raise RuntimeError(f"Stripe error: {e}")



def verify_webhook_signature(payload, sig_header):
    """
    Vérifie la signature Stripe
    
    Returns:
        event Stripe ou None si invalide
    """
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
        return event
    except Exception as e:
        print(f"❌ Signature invalide: {e}")
        return None

def handle_checkout_completed(session):
    return {
        "session_id": session["id"],
        "email": session.get("customer_email"),
        "amount": session["amount_total"],
        "metadata": session["metadata"],
    }



def handle_payment_failed(payment_intent):
    """Traite un paiement échoué"""
    print(f"❌ Paiement échoué: {payment_intent['id']}")
    return True


def handle_charge_refunded(charge):
    """Traite un remboursement"""
    print(f"💸 Remboursement: {charge['id']}")
    return True


def retrieve_session(session_id):
    """Récupère une session Stripe"""
    try:
        return stripe.checkout.Session.retrieve(session_id)
    except Exception as e:
        print(f"❌ Erreur récupération session: {e}")
        return None