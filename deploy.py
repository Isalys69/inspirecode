import os
import git

# Chemin correct vers votre répertoire de projet
project_dir = '/Users/isalys/my_project_env/inspirecode'

# Changez le répertoire de travail
os.chdir(project_dir)

# Pull les dernières modifications depuis GitHub
repo = git.Repo(project_dir)
repo.remotes.origin.pull()

# Installer les dépendances (si nécessaire)
os.system('pip install -r requirements.txt')

print("Déploiement terminé avec succès.")