import sys
import os

# Définir le chemin du projet
project_home = '/home/Isalys/inspirecode'

# Ajouter le chemin du projet au système si ce n'est pas déjà fait
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Importer l'application Flask depuis run.py
try:
    from run import app as application  # Assurez-vous que 'app' est bien défini dans run.py
except ImportError as e:
    raise ImportError(f"Impossible d'importer 'app' depuis run.py : {e}")

# Optionnel : définir des configurations spécifiques à l'environnement WSGI
application.config['ENV'] = 'production'
application.config['DEBUG'] = False  # Désactiver le mode débogage en production

# Journalisation pour WSGI
if not application.debug:
    import logging
    from logging.handlers import RotatingFileHandler

    log_file = os.path.join(project_home, 'logs/wsgi.log')
    os.makedirs(os.path.dirname(log_file), exist_ok=True)  # Crée le dossier logs si nécessaire
    handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=5)
    handler.setLevel(logging.INFO)
    application.logger.addHandler(handler)
    application.logger.info("Application WSGI chargée avec succès")
