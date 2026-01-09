from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask import send_from_directory
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

from datetime import date
from dateutil.relativedelta import relativedelta
import locale

from calendly import register_calendly_routes

import re


locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")



load_dotenv("config/.env")

app = Flask(__name__)

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

        if not email:
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
    return render_template("realisations.html")

@app.route("/realisations_sites_vitrines")
def realisations_sites_vitrines():
    return render_template("realisations/realisations_sites_vitrines.html")

@app.route("/realisations_sites_ecommerce")
def realisations_sites_ecommerce():
    return render_template("realisations/realisations_sites_ecommerce.html")



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
        if not email:
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



@app.route("/commander/site-vitrine-essentielle")
def commander_vitrine_essentielle():
    return render_template("offres/vitrine-essentielle.html")


@app.route("/commander/site-ecommerce-essentielle")
def commander_ecommerce_essentielle():
    return render_template("offres/ecommerce-essentielle.html")



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
def appmobile():
    return render_template("appmobile.html")

@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')

@app.route('/mentions-legales')
def mentionslegales():
    return render_template('mentions-legales.html')

@app.route('/politique-confidentialite')
def politiqueconfidentialite():
    return render_template('politique-confidentialite.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
