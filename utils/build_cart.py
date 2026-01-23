# utils/build_cart.py


ESSENTIELLES_CONFIG = {
    "vitrine-essentielle": {
        "label": "Essentielle – Site vitrine",
        "summary": "Création d’un site vitrine simple, professionnel et responsive, conçu pour présenter votre activité efficacement.",
        "base_price": 69000,
        "included": [
            "Modèle de site vitrine personnalisé",
            "Site vitrine de 3 pages",
            "Mise en ligne du site",
            "7 jours de support post-livraison (corrections mineures)"
        ],
        "excluded": [
            "Rédaction complète des contenus\n(les textes sont fournis par le client. Un accompagnement est possible pour la structuration)",
            "Création de logo ou d’identité visuelle complète,",
            "Maintenance évolutive",
            "Fonctionnalités spécifiques (réservation, e-commerce, espace membre…),",
            "Référencement avancé ou les campagnes publicitaires,",
            "Évolutions et la maintenance au-delà de la période incluse."
        ],
        "options": {
            "opt-devis": {"label": "Formulaire de devis avancé", "price": 15000},
            "opt-carte": {"label": "Carte interactive avec zone d’intervention", "price": 10000},
            "opt-page": {"label": "Page supplémentaire", "price": 9000},
            "opt-seo": {"label": "SEO de base", "price": 12000},
        },
    },

    "ecommerce-essentielle": 
        {
        "label": "Essentielle – Site eCommerce",
        "base_price": 89000,
        "summary": "Une solution eCommerce clé en main pour vendre en ligne simplement et efficacement.",
        "included": [
            "Boutique prête à vendre",
            "Design responsive",
            "Pages du parcours client",
            "Jusqu'à 20 produits",
            "Paiement sécurisé",
            "Livraison simple",
            "Interface administrative",
            "Mise en ligne",
        ],
        "excluded": [
            "Rédaction complète des contenus\n(les textes sont fournis par le client. Un accompagnement est possible pour la structuration)",
            "Création de logo ou d’identité visuelle complète,",
            "Fonctionnalités e-commerce avancées (abonnements, marketplace, multi-vendeurs…),",
            "Intégrations complexes (ERP, CRM, outils métier),",
            "Référencement avancé ou la publicité en ligne,",
            "Évolutions et la maintenance au-delà de la période incluse."
        ],
        "options": {
            "opt-produits": {"label": "Produits supplémentaires (jusqu’à 40)", "price": 12000},
            "opt-variables": {"label": "Produits variables", "price": 18000},
            "opt-livraison":{"label": "Livraison avancée", "price": 15000},
            "opt-emails":{"label": "Courriels transactionnels personalisés", "price": 12000},
            "opt-seo":{"label": "SEO eCommerce de base", "price": 15000},
            "opt-legale":{"label": "Pages légales eCommerce", "price": 9000}
        },
    },

    
    "appmobile-essentielle": 
        {
        "label": "Essentielle – Application mobile",
        "base_price": 49000,
        "summary": "Application mobile simple, responsive et prête à être publiée.",
        "included": [
            "Web app mobile",
            "Modèle éprouvé",
            "Jusqu'à 3 écrans / pages",
            "Usage principal défini",
            "Mise en ligne",
            "7 jours de support post-livraison (corrections mineures)"
        ],
        "excluded": [
            "Conception UX/UI avancée ou les tests utilisateurs approfondis,",
            "Fonctionnalités complexes (temps réel, géolocalisation avancée, IA, paiements intégrés…),",
            "Connexions à des systèmes externes complexes (API métier, ERP…),",
            "Publication sur les stores (si non prévue dans l’offre),",
            "Évolutions et la maintenance au-delà de la période incluse."
        ],
        "options": {
            "opt-desktop": {"label": "Adaptation pour usage desktop (outil)", "price": 40000},
            "opt-google": {"label": "Publication sur Google Play", "price": 25000},
            "opt-apple": {"label": "Publication sur Apple Store", "price": 35000},
            "opt-stores": {"label": "Publication sur deux stores (Google + Apple)", "price": 50000},
        }
    }
}

def build_essentielle(form_data, offre_code):
    config = ESSENTIELLES_CONFIG.get(offre_code)

    if not config:
        raise ValueError("Offre Essentielle inconnue")

    total = config["base_price"]
    options_display = []

    selected_options = form_data.getlist("options")

    for opt_id in selected_options:
        option = config["options"].get(opt_id)
        if option:
            total += option["price"]
            options_display.append({
                "label": option["label"],
                "price": option["price"],
            })

    pricing = {
        "amount_total": total,
        "currency": "eur",
        "display": f"{total // 100} € TTC",
    }

    return {
        "offre_code": offre_code,
        "label": config["label"],
        "summary": config["summary"],
        "included": config["included"],
        "excluded": config["excluded"],
        "options_display": options_display,
        "pricing": pricing,
    }
