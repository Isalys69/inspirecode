from flask import Flask, render_template, request, redirect, url_for
import subprocess

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


@app.route("/update", methods=["GET", "POST"])
def webhook():
    """
    Route pour gérer les webhooks GitHub ou les mises à jour via Postman.
    """
    if request.method == "POST":
        try:
            # Exécution du script de mise à jour
            result = subprocess.run(
                ["/home/Isalys/inspirecode/update.sh"], 
                check=True, 
                capture_output=True, 
                text=True
            )
            return f"Updated successfully! Output:\n{result.stdout}", 200
        except subprocess.CalledProcessError as e:
            # Capture les erreurs liées à `subprocess.run`
            return f"Error during script execution: {e.stderr}", 500
        except Exception as e:
            # Capture toute autre erreur
            return f"Unexpected error: {str(e)}", 500
    elif request.method == "GET":
        # Réponse explicative pour les requêtes GET
        return "This route is designed for POST requests to trigger updates. Please use POST.", 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
