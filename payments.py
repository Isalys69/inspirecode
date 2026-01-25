"""
Gestion des paiements Stripe
- Création de sessions Checkout
- Réception et traitement des webhooks Stripe
"""

import os
import stripe

from flask import current_app
from flask_mail import Message

def send_order_confirmation_email(email, order_label, amount):
    mail = current_app.extensions["mail"]

    subject = "Confirmation de votre commande – Inspire Code"

    body = f"""
Bonjour,

Merci pour votre commande.

✅ Offre : {order_label}
💳 Montant réglé : {amount / 100:.2f} €
📅 Date : aujourd'hui

Votre projet est officiellement lancé.
Je vous recontacte très rapidement pour la suite.

À très bientôt,
Isalys
Inspire Code
"""

    msg = Message(
        subject=subject,
        recipients=[email],
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
        body=body,
    )

    print("📨 Tentative envoi email vers :", email)
    print("📨 Expéditeur :", current_app.config["MAIL_DEFAULT_SENDER"])


    mail.send(msg)


# -------------------------------------------------------------------
# Configuration Stripe
# -------------------------------------------------------------------

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
if not stripe.api_key:
    raise RuntimeError("STRIPE_SECRET_KEY is not set")

try:
    account = stripe.Account.retrieve()
    print("STRIPE BACKEND ACCOUNT ID =", account["id"])
except Exception as e:
    print("STRIPE BACKEND ACCOUNT ERROR =", e)


STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
if not STRIPE_WEBHOOK_SECRET:
    raise RuntimeError("STRIPE_WEBHOOK_SECRET is not set")


# -------------------------------------------------------------------
# Création de session Checkout (Application → Stripe)
# -------------------------------------------------------------------

def create_checkout_session(*, order: dict, base_url: str) -> str:
    try:
        session = stripe.checkout.Session.create(
            mode="payment",

            payment_method_types=["card"],

            line_items=[{
                "price_data": {
                    "currency": order["pricing"]["currency"],
                    "product_data": {
                        "name": order["label"],
                    },
                    "unit_amount": order["pricing"]["amount_total"],
                },
                "quantity": 1,
            }],

            # 🔑 OBLIGATOIRE pour avoir l'email
            customer_creation="always",
            billing_address_collection="required",

            success_url=f"{base_url}/paiement/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{base_url}/commander/confirmation",

            locale="fr",
            metadata=order.get("metadata", {}),
        )

        return session.url

    except Exception as e:
        raise RuntimeError(f"Stripe checkout error: {e}") from e


# -------------------------------------------------------------------
# Webhook Stripe (Stripe → Backend)
# -------------------------------------------------------------------

def handle_stripe_webhook(payload: bytes, sig_header: str):
    """
    Point d'entrée métier pour les webhooks Stripe.
    - Valide la signature
    - Route l'événement vers le bon handler
    - Lève une exception si invalide (Flask renverra 400)
    """

    # Validation de signature (OBLIGATOIRE)
    event = stripe.Webhook.construct_event(
        payload=payload,
        sig_header=sig_header,
        secret=STRIPE_WEBHOOK_SECRET
    )

    event_type = event["type"]
    data = event["data"]["object"]

    if event_type == "checkout.session.completed":
        return handle_checkout_completed(data)

    elif event_type == "payment_intent.payment_failed":
        return handle_payment_failed(data)

    elif event_type == "charge.refunded":
        return handle_charge_refunded(data)

    # Événement non pertinent → accepté quand même
    return None


# -------------------------------------------------------------------
# Handlers métier
# -------------------------------------------------------------------

def handle_checkout_completed(session: dict):
    """
    Traitement d'un paiement réussi (checkout.session.completed)
    """

    email = None

    # 1. Email directement dans la session (rare mais possible)
    if session.get("customer_details"):
        email = session["customer_details"].get("email")

    # 2. Sinon, récupération depuis le Customer Stripe (cas normal)
    if not email and session.get("customer"):
        try:
            customer = stripe.Customer.retrieve(session["customer"])
            email = customer.get("email")
        except Exception as e:
            print("❌ Erreur récupération customer Stripe :", e)

    print("✅ Paiement confirmé")
    print("Session :", session.get("id"))
    print("Email final :", email)
    print("Montant :", session.get("amount_total"))
    print("Metadata :", session.get("metadata"))

    if not email:
        print("⚠️ Aucun email client trouvé → webhook accepté sans email")
        return True

    # 👉 ICI ton envoi d’email transactionnel
    send_order_confirmation_email(
        email=email,
        order_label=session.get("metadata", {}).get("offre_code", "Offre Inspire Code"),
        amount=session.get("amount_total"),
    )

    print("📧 Email transactionnel envoyé à", email)
    return True


def handle_payment_failed(payment_intent: dict):
    """
    Traitement d'un paiement échoué
    """
    print(f"❌ Paiement échoué: {payment_intent['id']}")
    return True


def handle_charge_refunded(charge: dict):
    """
    Traitement d'un remboursement
    """
    print(f"💸 Remboursement effectué: {charge['id']}")
    return True


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def retrieve_session(session_id: str):
    """
    Récupère une session Stripe Checkout par son ID
    """
    try:
        return stripe.checkout.Session.retrieve(session_id)
    except Exception as e:
        print(f"❌ Erreur récupération session: {e}")
        return None
