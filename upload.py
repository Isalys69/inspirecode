import os
import requests
import subprocess

# Vos informations
USERNAME = "Isalys"  # Votre nom d'utilisateur PythonAnywhere
APP_NAME = "www.inspirecode.fr"  # Le nom de votre application web
PROJECT_PATH = "."  # Le chemin de votre projet sur PythonAnywhere
WSGI_FILE = "/var/www/www_inspirecode_fr_wsgi.py"  # Le chemin du fichier WSGI
API_TOKEN = "2edf0ead08324cdea8930ee3af5e7750674ed46c"  # Remplacez par votre token d'API PythonAnywhere

# URL de l'API PythonAnywhere
API_BASE_URL = f"https://www.pythonanywhere.com/api/v0/user/{USERNAME}/"

def pull_latest_code():
    """Télécharge le dernier code depuis GitHub."""
    print("Téléchargement du dernier code depuis GitHub...")
    try:
        subprocess.run(["git", "pull", "origin", "main"], cwd=PROJECT_PATH, check=True)
        print("Code téléchargé avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du téléchargement du code : {e}")
        exit(1)

def restart_application():
    """Redémarre l'application web via l'API PythonAnywhere."""
    print("Redémarrage de l'application web...")
    url = f"{API_BASE_URL}webapps/{APP_NAME}/reload/"
    headers = {"Authorization": f"Token {API_TOKEN}"}
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        print("Application redémarrée avec succès.")
    else:
        print(f"Erreur lors du redémarrage de l'application : {response.status_code} - {response.text}")
        exit(1)

def touch_wsgi_file():
    """Modifie le fichier WSGI pour forcer le redémarrage du serveur."""
    print("Modification du fichier WSGI...")
    try:
        with open(WSGI_FILE, "a"):
            os.utime(WSGI_FILE, None)
        print("Fichier WSGI modifié avec succès.")
    except Exception as e:
        print(f"Erreur lors de la modification du fichier WSGI : {e}")
        exit(1)

def main():
    print("Début du déploiement...")
    pull_latest_code()
    touch_wsgi_file()
    restart_application()
    print("Déploiement terminé avec succès !")

if __name__ == "__main__":
    main()