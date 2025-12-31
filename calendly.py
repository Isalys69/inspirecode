# calendly.py
from flask import render_template, request, redirect, url_for

def register_calendly_routes(app):

    @app.route("/book", methods=["GET"])
    def book():
        return render_template("offres/calendly.html",
            hero_title="Faisons le point sur votre projet",
            hero_subtitle=(
                "Un échange de 15 minutes, gratuit et sans engagement, afin de :"
            ),
            hero_list=[
                " ✔ Clarifier votre besoin",
                " ✔ Valider la faisabilité technique",
                " ✔ Estimer un budget et des délais réalistes"
            ],
            cta_title="Aucun créneau ne vous convient ?",
            cta_url="contact",
            cta_button="Proposer mes disponibilités"
            )

    @app.route("/submit", methods=["POST"])
    def submit():
        email = request.form.get("email")
        # traitement éventuel
        return redirect(url_for("book"))
