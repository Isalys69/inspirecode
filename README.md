# 🌐 Inspire Code  
** Développement Web, App. mobile & Automatisations **

![Logo Inspire Code](static/images/logo.png)

Inspire Code est une micro-entreprise spécialisée dans :  
- la création de **sites vitrines élégants et rapides**,  
- le développement de **sites e-commerce simples et efficaces**,  
- la réalisation d’**automatisations et scripts** pour optimiser le travail des indépendants,  
- et la mise en place d’**applications web personnalisées**.

L’objectif : créer des solutions **claires, durables, performantes** pour les entrepreneurs et petites structures de l’ouest lyonnais.

---

## 🚀 Technologies utilisées

Ce projet utilise les technologies suivantes :

- **Python 3.x**
- **Flask** (framework web léger et puissant)
- **Jinja2** (templates HTML dynamiques)
- **Bootstrap 5** (mise en page responsive)
- **OVH Mail** (envoi d’e-mails professionnels)
- **PythonAnywhere** (hébergement)
- **Git & GitHub** (versioning et déploiement manuel)

---

## 🗂️ Architecture du projet

Structure principale :

- `run.py` : point d’entrée Flask. Charge les variables d’environnement depuis `config/.env`, configure l’envoi d’e-mails (Flask-Mail) et déclare les routes des pages.
- `templates/` : pages HTML Jinja2 (accueil, services, formulaires, pages légales).
- `static/` : assets statiques (CSS, JS, images, favicon, robots.txt).
- `config/` (attendu) : contient le fichier `.env` avec les secrets Flask et les paramètres SMTP (ex. `FLASK_SECRET_KEY`, `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER`, `MAIL_RECIPIENT`, `MAIL_USE_TLS`, `MAIL_USE_SSL`).
- `requirements.txt` : dépendances Python nécessaires à l’exécution.

## ▶️ Démarrage & déploiement

1. Créer un environnement virtuel puis installer les dépendances :
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Ajouter un fichier `config/.env` en reprenant les variables listées ci-dessus.
3. Lancer le serveur local sur http://localhost:5000/ :
   ```bash
   python run.py
   ```
4. Pour un déploiement (ex. PythonAnywhere), reprendre cette structure : copier `run.py`, le dossier `templates/`, `static/`, `requirements.txt` et le `config/.env` adapté à l’environnement d’hébergement.

## 📬 Contact
Pour toute demande :
📧 contact@inspirecode.fr
🌐 Site : https://www.inspirecode.fr


## 🛡️ Licence
Projet propriétaire – © 2024-2025 Inspire Code.
Toute reproduction ou réutilisation du code sans autorisation est interdite.
