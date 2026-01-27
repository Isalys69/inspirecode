import os
from dotenv import load_dotenv

if os.getenv("FLASK_ENV") != "production":
    load_dotenv(dotenv_path="config/.env", override=True)
    '''
    print("FLASK_ENV =", os.getenv("FLASK_ENV"))
    print("STRIPE_SECRET_KEY =", os.getenv("STRIPE_SECRET_KEY"))
    print("STRIPE_WEBHOOK_SECRET =", os.getenv("STRIPE_WEBHOOK_SECRET"))
    '''

from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
import payments
from payments import create_checkout_session

from flask import send_from_directory
from flask_mail import Mail, Message
from zoneinfo import ZoneInfo
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import locale

from calendly import register_calendly_routes

import json
from utils.build_cart import build_essentielle
import re



locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")





app = Flask(__name__)
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")




# Configuration de Flask-Mail
# Chargement SMTP depuis les variables d’environnement
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))

# Gestion propre de TLS / SSL
def str_to_bool(value):
    return value.lower() in ("true", "1", "yes", "y")

app.config['MAIL_USE_TLS'] = str_to_bool(os.getenv('MAIL_USE_TLS', 'true'))
app.config['MAIL_USE_SSL'] = str_to_bool(os.getenv('MAIL_USE_SSL', 'false'))

if app.config['MAIL_USE_TLS'] and app.config['MAIL_USE_SSL']:
    raise ValueError("MAIL_USE_TLS et MAIL_USE_SSL ne peuvent pas être activés simultanément.")

# Authentification SMTP
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')


# Destinataires
raw_recipients = os.getenv('MAIL_RECIPIENT')

if not raw_recipients:
    app.logger.error("MAIL_RECIPIENT est requis pour envoyer des emails.")
    raise ValueError("MAIL_RECIPIENT doit être défini avec au moins un destinataire.")

raw_recipient_entries = [recipient.strip() for recipient in raw_recipients.split(',')]
recipients = [recipient for recipient in raw_recipient_entries if recipient]

if len(raw_recipient_entries) != len(recipients):
    app.logger.warning("Certaines entrées vides dans MAIL_RECIPIENT ont été ignorées.")

if not recipients:
    app.logger.error("Aucun destinataire valide n'a été trouvé dans MAIL_RECIPIENT.")
    raise ValueError("La liste des destinataires est vide après le filtrage des valeurs vides.")

app.logger.info("Destinataires configurés : %s", ", ".join(recipients))
app.config['RECIPIENTS'] = recipients
mail = Mail(app)





# injection des routes Calendly
register_calendly_routes(app)

@app.route("/devis", methods=["GET", "POST"])
def devis():
    invalid_fields = []
    form_data = {}

    if request.method == "POST":
        form_data = request.form

        # Récupération sécurisée
        prenom = form_data.get("prenom", "").strip()
        nom = form_data.get("nom", "").strip()
        email = form_data.get("email", "").strip()
        telephone = form_data.get("telephone", "").strip()
        type_projet = form_data.get("type_projet", "")
        budget = form_data.get("budget", "")
        delais = form_data.get("delais", "")
        message = form_data.get("message", "").strip()
        rgpd = form_data.get("rgpd")

        # VALIDATION (clé du comportement visuel)
        if not prenom:
            invalid_fields.append("prenom")

        if not nom:
            invalid_fields.append("nom")

        email_regex = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        if not email or not re.match(email_regex, email):
            invalid_fields.append("email")

        if not type_projet:
            invalid_fields.append("type_projet")

        if not budget:
            invalid_fields.append("budget")

        if not delais:
            invalid_fields.append("delais")

        if not message:
            invalid_fields.append("message")

        if not rgpd:
            invalid_fields.append("rgpd")

        # S'il y a des erreurs → on réaffiche le formulaire
        if invalid_fields:
            return render_template(
                "devis.html",
                invalid_fields=invalid_fields,
                form_data=form_data
            )

        # =====================
        # ENVOI EMAIL (OK)
        # =====================

        subject = f"[Inspire Code] Demande de devis – {nom}"
        body = f"""
Nouvelle demande de devis Inspire Code :

Prénom : {prenom}
Nom : {nom}
Email : {email}
Téléphone : {telephone or 'Non précisé'}

Type de projet : {type_projet}
Budget souhaité : {budget}
Délais : {delais}

Message :
{message}
"""

        msg = Message(
            subject=subject,
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=app.config['RECIPIENTS'],
            body=body
        )

        try:
            mail.send(msg)

            flash("Votre demande de devis a bien été envoyée. Je reviens vers vous sous 24h.", "success")
            return redirect(url_for("devis"))
        except Exception as e:
            flash(f"Erreur lors de l'envoi : {e}", "danger")
            return redirect(url_for("devis"))

    # GET
    referrer = request.referrer
    if referrer and not referrer.endswith("/devis"):
        session["previous_page"] = referrer

    return render_template("devis.html")



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/offres")
def offres():
    return render_template("offres.html")

@app.route("/realisations")
def realisations():
    return render_template(
        "realisations.html",
        show_automatisations=False
    )

@app.route("/realisations_sites_vitrines")
def realisations_sites_vitrines():
    return render_template("realisations/realisations_sites_vitrines.html")

@app.route("/realisations_sites_ecommerce")
def realisations_sites_ecommerce():
    return render_template("realisations/realisations_sites_ecommerce.html")

@app.route("/realisations_appmobiles")
def realisations_appmobiles():
    return render_template("realisations/realisations_appmobiles.html")





@app.route("/contact", methods=["GET", "POST"])
def contact():
    erreurs = []

    if request.method == "POST":
        prenom = request.form.get("prenom", "").strip()
        nom = request.form.get("nom", "").strip()
        email = request.form.get("email", "").strip()
        sujet = request.form.get("sujet", "").strip()
        message = request.form.get("message", "").strip()

        if not prenom:
            erreurs.append("prenom")
        if not nom:
            erreurs.append("nom")

        # ✅ contrôle email (vide + format simple)
        email_regex = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        if not email or not re.match(email_regex, email):
            erreurs.append("email")

        if not sujet:
            erreurs.append("sujet")
        if not message:
            erreurs.append("message")

        if erreurs:
            return render_template(
                "contact.html",
                invalid_fields=erreurs,
                form_data=request.form
            )

        msg = Message(
            subject=f"[Contact Inspire Code] {sujet}",
            recipients=app.config['RECIPIENTS'],
            reply_to=email
        )

        msg.body = f"""
Nouveau message via le site Inspire Code

Prénom : {prenom}
Nom : {nom}
Email : {email}

Message :
{message}
"""
        try:
            mail.send(msg)
            flash("Votre message a bien été envoyé. Je vous répondrai rapidement.", "success")
            return redirect(url_for("contact"))

        except Exception as e:
            flash(f"Erreur lors de l'envoi : {e}", "danger")
            return redirect(url_for("contact"))

    # GET
    referrer = request.referrer
    if referrer and not referrer.endswith("/contact"):
        session["previous_page"] = referrer

    return render_template("contact.html")


@app.route("/offres/site-vitrine")
def offre_site_vitrine():
    try:
        locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
    except locale.Error:
        pass

    mois_disponible = (date.today() + relativedelta(months=1)).strftime("%B").capitalize()
    return render_template(
        "offres/site-vitrine.html",

        hero_title="Site vitrine professionnel",
        hero_subtitle="Une présence en ligne claire, crédible et alignée avec votre activité.",

        cta_title="Besoin d'aide pour choisir ?",
        cta_url="book",
        cta_button="📅 Réserver un appel conseil de 15 min",
        mois_disponible=mois_disponible

    )


@app.route("/offres/site-ecommerce")
def offre_site_ecommerce():
    try:
        locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
    except locale.Error:
        pass

    mois_disponible = (date.today() + relativedelta(months=1)).strftime("%B").capitalize()
    return render_template(
        "offres/site-ecommerce.html",

        hero_title="Site eCommmerce professionnel",
        hero_subtitle="Une boutique en ligne claire et fiable pour vendre vos produits.",

        cta_title="Besoin d'aide pour choisir ?",
        cta_url="book",
        cta_button="📅 Réserver un appel conseil de 15 min",
        mois_disponible=mois_disponible

    )



@app.route("/commander/site-vitrine-essentielle", methods=["GET", "POST"])
def commander_vitrine_essentielle():

    if request.method == "POST":
        print("FORM DATA :", request.form)
        # 2. Construire / mettre à jour le cart
        cart = build_essentielle(
            request.form,
            "vitrine-essentielle"
            )
        # 3. Stocker le cart (normalisé)
        session["cart"] = cart

        # 4. Redirection vers confirmation
        return redirect(url_for("commander_confirmation"))

    # GET : affichage de la page offre
    return render_template("offres/vitrine-essentielle.html")


@app.route("/commander/site-ecommerce-essentielle", methods=["GET", "POST"])
def commander_ecommerce_essentielle():

    if request.method == "POST":
        print("FORM DATA :", request.form)

        # 2. Construire / mettre à jour le cart
        cart = build_essentielle(
            request.form,
            "ecommerce-essentielle"
            )
        # 3. Stocker le cart (normalisé)
        session["cart"] = cart

        # 4. Redirection vers confirmation
        return redirect(url_for("commander_confirmation"))

    # GET : affichage de la page offre
    return render_template("offres/ecommerce-essentielle.html")


@app.route("/commander/appmobile-essentielle", methods=["GET", "POST"])
def commander_appmobile_essentielle():

    if request.method == "POST":
        print("FORM DATA :", request.form)
        # 2. Construire / mettre à jour le cart
        cart = build_essentielle(
            request.form,
            "appmobile-essentielle"
            )
        # 3. Stocker le cart (normalisé)
        session["cart"] = cart

        # 4. Redirection vers confirmation
        return redirect(url_for("commander_confirmation"))

    # GET : affichage de la page offre
    return render_template("offres/appmobile-essentielle.html")



@app.route("/commander/confirmation", methods=["GET", "POST"])
def commander_confirmation():


    cart = session.get("cart")
    if not cart:
        abort(400, "Commande expirée ou invalide.")

    order = {
        "label": cart["label"],
        "summary": cart.get("summary"),
        "included": cart["included"],
        "excluded": cart.get("excluded"),
        "options": cart["options_display"],
        "pricing": cart["pricing"],
        "meta": {
            "offre_code": cart["offre_code"],
            "renonciation_required": True
        }
    }

    return render_template(
        "commander/confirmation.html",
        order=order,
        hero_title="Confirmation de votre commande",
        hero_subtitle="Merci de vérifier les éléments ci-dessous.\n Le paiement vous permettra de lancer immédiatement votre projet."

    )




@app.route("/paiement/checkout", methods=["POST"])
def checkout():
    """
    Crée une session Stripe après validation finale
    """

    # 1. Vérifier la renonciation
    if request.form.get("accept_renonciation") != "1":
        abort(400, "Renonciation au droit de rétractation non acceptée.")

    # 2. Vérifier l'existence du cart
    cart = session.get("cart")
    if not cart:
        abort(400, "Commande introuvable ou expirée.")

    # 3. Reconstruire l'order (source unique)
    order = {
        "label": cart["label"],
        "pricing": cart["pricing"],
        "metadata": {
            "offre_code": cart["offre_code"],
            "renonciation": "accepted",
        }
    }

    # 4. Vérifier le montant attendu (anti-tampering)
    try:
        amount_expected = int(request.form.get("amount_expected", 0))
    except ValueError:
        abort(400, "Montant invalide.")

    if amount_expected != order["pricing"]["amount_total"]:
        abort(400, "Incohérence de montant détectée.")

    # 5. Créer la session Stripe

    try:
        print("HOST_URL =", request.host_url)

        checkout_url = create_checkout_session(
            order=order,
            base_url=request.host_url.rstrip("/")
        )
    except Exception as e:
        abort(500, str(e))

    # 6. Redirection vers Stripe Checkout
    return redirect(checkout_url)

@app.route("/paiement/success")
def paiement_success():
    session_id = request.args.get("session_id")

    if not session_id:
        abort(400, "Session Stripe manquante.")

    return render_template(
        "paiement/succes.html",
        session_id=session_id,
        date=datetime.now(ZoneInfo("Europe/Paris"))
    )


@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    print(">>> WEBHOOK REÇU <<<")
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    try:
        payments.handle_stripe_webhook(payload, sig_header)
    except Exception as e:
        import traceback
        print("❌ ERREUR WEBHOOK DÉTAILLÉE")
        traceback.print_exc()
        return "", 400

    return "", 200


@app.route("/offres/automatisations")
def offre_automatisations():
    try:
        locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
    except locale.Error:
        pass

    mois_disponible = (date.today() + relativedelta(months=1)).strftime("%B").capitalize()


    return render_template("offres/automatisations.html",

        hero_title="Automatisations professionnelles",
        hero_subtitle="Des automatisations claires et fiables pour simplifier votre quotidien.",

        cta_title="Besoin d'aide pour choisir ?",
        cta_url="book",
        cta_button="📅 Réserver un appel conseil de 15 min",
        mois_disponible=mois_disponible

    )

@app.route("/appmobile")
def offre_appmobile():
    try:
        locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
    except locale.Error:
        pass

    mois_disponible = (date.today() + relativedelta(months=1)).strftime("%B").capitalize()

    return render_template("/offres/appmobile.html",


        hero_title="Applications mobiles professionnelles",
        hero_subtitle="Une application mobile claire et fiable pour répondre à un usage précis.",

        cta_title="Besoin d'aide pour choisir ?",
        cta_url="book",
        cta_button="📅 Réserver un appel conseil de 15 min",
        mois_disponible=mois_disponible
    )


@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/mentions-legales')
def mentionslegales():
    return render_template('/legales/mentions-legales.html')

@app.route('/politique-confidentialite')
def politiqueconfidentialite():
    return render_template('/legales/politique-de-confidentialite.html')

@app.route('/cgv')
def cgv():
    return render_template('/legales/cgv.html')

'''
if __name__ == "__main__":
    app.run(debug=True, port=5000)
'''

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )

