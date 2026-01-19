# utils/build_cart.py

def build_cart_vitrine_essentielle(selected_options):
    BASE_PRICE = 69000  # centimes

    OPTIONS_CONFIG = {
        "opt-devis": {
            "label": "Formulaire de devis avancé",
            "price": 15000,
        },
        "opt-carte": {
            "label": "Carte + zone d’intervention",
            "price": 10000,
        },
        "opt-page": {
            "label": "Page supplémentaire",
            "price": 9000,
        },
        "opt-seo": {
            "label": "SEO de base",
            "price": 12000,
        },
    }

    total = BASE_PRICE
    options_display = []

    for opt_id in selected_options:
        if opt_id in OPTIONS_CONFIG:
            opt = OPTIONS_CONFIG[opt_id]
            total += opt["price"]
            options_display.append({
                "label": opt["label"],
                "price_label": f"+{opt['price'] // 100} €",
            })

    return {
        "offre_code": "vitrine-essentielle",
        "label": "Pack Essentielle – Site vitrine",
        "summary": "Création d’un site vitrine professionnel, responsive et prêt à être mis en ligne.",
        "included": [
            "Structure du site",
            "Design responsive",
            "Mise en ligne",
        ],
        "excluded": [
            "Rédaction des contenus",
            "Hébergement",
            "Maintenance évolutive",
        ],
        "options_display": options_display,
        "pricing": {
            "amount_total": total,
            "currency": "eur",
            "display": f"{total // 100} € TTC",
        },
    }
