from flask import Flask, render_template, request, redirect, url_for, flash
from flask import send_from_directory
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

from datetime import date
from dateutil.relativedelta import relativedelta
import locale

locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")



load_dotenv("config/.env")

app = Flask(__name__)

app.secret_key = os.getenv('FLASK_SECRET_KEY')


# Configuration de Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))


def str_to_bool(value):
    return value.lower() in ("true", "1", "yes", "y")

app.config['MAIL_USE_TLS'] = str_to_bool(os.getenv('MAIL_USE_TLS', 'true'))
app.config['MAIL_USE_SSL'] = str_to_bool(os.getenv('MAIL_USE_SSL', 'false'))


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

print("SMTP =", app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
print("EMAIL =", app.config['MAIL_USERNAME'])
print("PASSWORD =", app.config['MAIL_PASSWORD'])
print("DEFAULT SENDER =", app.config['MAIL_DEFAULT_SENDER'])




@app.route("/devis", methods=["GET", "POST"])
def devis():
    if request.method == "POST":

        print("📩 FORM DATA REÇU PAR FLASK :", request.form)


        nom = request.form['nom']
        email = request.form['email']
        telephone = request.form.get('telephone', 'Non précisé')
        type_projet = request.form['type_projet']
        budget = request.form['budget']
        delais = request.form['delais']
        message = request.form['message']

        subject = f"[Inspire Code] Demande de devis – {nom}"
        body = f"""
Nouvelle demande de devis Inspire Code :

Nom : {nom}
Email : {email}
Téléphone : {telephone}

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
            print("📨 TENTATIVE D'ENVOI D'EMAIL VIA FLASK-MAIL...")
            flash("Votre demande de devis a bien été envoyée. Je reviens vers vous sous 24h.", "success")
        except Exception as e:
            print("❌ ERREUR FLASK-MAIL :", e)
            flash(f"Erreur lors de l'envoi : {e}", "danger")

        return redirect(url_for("devis"))

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

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        nom = request.form.get("nom")
        email = request.form.get("email")
        sujet = request.form.get("sujet")
        message = request.form.get("message")

        # Exemple : traitement, envoi email, stockage, etc.
        print("NOUVEAU MESSAGE :", nom, email, sujet, message)

        # Futur : flash message de confirmation, redirection, etc.
        return render_template("contact.html", success=True)

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
        cta_button="📅 Réserver un appel conseil de 15 min - Sans engagement",
        mois_disponible=mois_disponible

    )





@app.route("/commander/site-vitrine-essentielle")
def commander_vitrine_essentielle():
    return render_template("offres/vitrine-essentielle.html")

@app.route("/ecommerce")
def ecommerce():
    return render_template("ecommerce.html")

@app.route("/automatisations")
def automatisations():
    return render_template("automatisations.html")

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
