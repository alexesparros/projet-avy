# Fonctions de recommandation pour le projet AVY

def recommander_jeux_via_ia(prompt, model):
    """Exemple de fonction pour générer des recommandations de jeux via un modèle IA."""
    reco_chunks = model.generate_content(prompt, stream=True)
    recommandations_brutes = ""
    for chunk in reco_chunks:
        recommandations_brutes += chunk.text
    return recommandations_brutes 