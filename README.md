# Projet AVY - Plateforme d'analyse et de recommandation de jeux vidéo

## Structure du projet

```
projet-avy/
│
├── app.py                  # Point d'entrée Streamlit
├── pages/                  # Pages Streamlit (accueil, inscription, etc.)
├── utils/                  # Fonctions utilitaires modulaires
│   ├── data_loader.py      # Chargement des données
│   ├── preprocessing.py    # Nettoyage et préparation des données
│   ├── recommender.py      # Fonctions de recommandation
│   ├── plotting.py         # Fonctions de visualisation
│   └── helpers.py          # Fonctions utilitaires génériques
├── keys.py                 # Clés et tokens API (à créer, à ne pas versionner)
├── requirements.txt        # Dépendances Python
├── README.md               # Ce fichier
├── ...
```

## Rôle du dossier `utils/`
Ce dossier regroupe toutes les fonctions réutilisables du projet :
- Chargement et sauvegarde de données
- Nettoyage et transformation
- Calculs de scores, recommandations
- Visualisations
- Fonctions utilitaires diverses

## Où placer les clés ?
Créez un fichier `keys.py` à la racine du projet, par exemple :
```python
STEAM_API_KEY = "votre_clé_steam"
AUTRE_TOKEN = "..."
```
Ce fichier ne doit pas être versionné (ajoutez-le à `.gitignore`).

## Lancer le projet
1. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
2. Lancez l'application :
   ```bash
   streamlit run app.py
   ```

---

## Ressources et documentations utiles

- [Documentation Streamlit](https://docs.streamlit.io/)
- [API RAWG (jeux vidéo)](https://rawg.io/apidocs)
- [Google Gemini API (Generative AI)](https://ai.google.dev/)
- [Documentation Python officielle](https://docs.python.org/3/)
- [Documentation Pandas](https://pandas.pydata.org/docs/)
- [Documentation Matplotlib](https://matplotlib.org/stable/contents.html)

Pour toute question ou contribution, n’hésitez pas à consulter ces ressources ou à demander de l’aide ! 