from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    """
    Page d'accueil
    """
    return render_template("index.html")

@app.route("/about")
def about():
    """
    Page À propos
    """
    return render_template("about.html")

@app.route("/services")
def services():
    """
    Page Services
    """
    return render_template("services.html")

@app.route("/portfolio")
def portfolio():
    """
    Page Portfolio
    """
    return render_template("portfolio.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    """
    Page Contact - Gère aussi le formulaire
    """
    if request.method == "POST":
        # Exemple : traiter les données du formulaire (désactivé ici)
        # nom = request.form.get("name")
        # email = request.form.get("email")
        # message = request.form.get("message")
        # TODO: traiter les données (envoi d'email, stockage, etc.)
        return redirect(url_for("contact"))  # On peut rediriger vers la page contact ou home
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
