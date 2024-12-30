import os
import requests
import subprocess
import getpass


# Vos informations
USERNAME = "Isalys"  # Votre nom d'utilisateur PythonAnywhere
APP_NAME = "www.inspirecode.fr"  # Le nom de votre application web
# PROJECT_PATH = "/home/Isalys/inspirecode"  # Le chemin de votre projet sur PythonAnywhere
WSGI_FILE = "/var/www/www_inspirecode_fr_wsgi.py"  # Le chemin du fichier WSGI
API_TOKEN = "2edf0ead08324cdea8930ee3af5e7750674ed46c"  # Remplacez par votre token d'API PythonAnywhere

# URL de l'API PythonAnywhere
API_BASE_URL = f"https://www.pythonanywhere.com/api/v0/user/{USERNAME}/"

# Détection de l'environnement
if "GITHUB_ACTIONS" in os.environ:
    # Environnement GitHub Actions
    PROJECT_PATH = os.getcwd()
else:
    # Environnement PythonAnywhere
    PROJECT_PATH = "/home/Isalys/inspirecode"

print(f"Chemin du projet : {PROJECT_PATH}")

# Tentative de récupération robuste de l'utilisateur
try:
    user = os.getlogin()
except OSError:
    user = os.getenv("USER") or os.getenv("LOGNAME") or getpass.getuser()

print(f"Utilisateur actuel : {user}")



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
    """Utilise l'API PythonAnywhere pour forcer la modification du fichier WSGI."""
    print("Modification du fichier WSGI via l'API PythonAnywhere...")
    url = f"{API_BASE_URL}files/path{WSGI_FILE}"
    headers = {"Authorization": f"Token {API_TOKEN}"}
    new_content = "# Modification via API\n"
    
    response = requests.post(
        url,
        headers=headers,
        files={"content": new_content},
    )

    if response.status_code == 200:
        print("Fichier WSGI modifié avec succès.")
    else:
        print(f"Erreur lors de la modification du fichier WSGI : {response.status_code} - {response.text}")
        exit(1)

def main():
    print("Début du déploiement...")
    pull_latest_code()
    touch_wsgi_file()
    restart_application()
    print("Déploiement terminé avec succès !")

if __name__ == "__main__":
    main()