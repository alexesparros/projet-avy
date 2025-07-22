# Fonctions de nettoyage et de préparation des données pour le projet AVY

import ast
import re
import pandas as pd

# --- Fonctions de parsing et nettoyage Steam ---
def parse_str_to_dict_or_list(x):
    """Convertit une chaîne en dictionnaire ou liste Python."""
    try:
        return ast.literal_eval(x) if isinstance(x, str) else x
    except:
        return None

def get_nested_value(x, key):
    """Extrait une clé d’un dictionnaire."""
    x = parse_str_to_dict_or_list(x)
    return x.get(key) if isinstance(x, dict) else None

def get_list_descriptions(x):
    """Extrait toutes les 'description' d'une liste de dictionnaires."""
    x = parse_str_to_dict_or_list(x)
    return ", ".join([item["description"] for item in x if "description" in item]) if isinstance(x, list) else None

def clean_list_to_string(x):
    """Transforme une liste en texte propre sans crochets ni guillemets."""
    x = parse_str_to_dict_or_list(x)
    return ", ".join(x) if isinstance(x, list) else str(x)

def extract_date(x):
    """Extrait la date depuis un dictionnaire contenant une clé 'date'."""
    x = parse_str_to_dict_or_list(x)
    return x.get("date") if isinstance(x, dict) else None

def clean_languages(x):
    """Supprime les balises HTML dans les langues supportées."""
    return re.sub(r"<.*?>", "", x) if isinstance(x, str) else x

# --- Fonctions de pipeline de nettoyage ---
def safe_extract_date(x):
    try:
        if isinstance(x, dict):
            return x.get("date")
        elif isinstance(x, str):
            parsed = ast.literal_eval(x)
            if isinstance(parsed, dict):
                return parsed.get("date")
    except:
        return None

def clean_steam_data(df):
    # Étape 1 : supprimer les colonnes inutiles
    columns_to_drop = [
        "background", "background_raw", "capsule_imagev5", "demos", "dlc",
        "legal_notice", "package_groups", "packages", "reviews",
        "screenshots", "support_info"
    ]
    df_clean = df.drop(columns=columns_to_drop, errors="ignore")

    # Étape 2 : supprimer doublons et lignes sans nom
    df_clean = df_clean.drop_duplicates()
    df_clean = df_clean[df_clean["name"].notna() & (df_clean["name"] != "")]

    # Étape 3 : nettoyage des colonnes imbriquées
    df_clean["achievements"] = df_clean["achievements"].apply(lambda x: get_nested_value(x, "total"))
    df_clean["categories"] = df_clean["categories"].apply(get_list_descriptions)
    df_clean["genres"] = df_clean["genres"].apply(get_list_descriptions)
    df_clean["content_descriptors"] = df_clean["content_descriptors"].apply(lambda x: get_nested_value(x, "notes"))
    df_clean["developers"] = df_clean["developers"].apply(clean_list_to_string)
    if "publishers" in df_clean.columns:
        df_clean["publishers"] = df_clean["publishers"].apply(clean_list_to_string)
    df_clean["metacritic"] = df_clean["metacritic"].apply(lambda x: get_nested_value(x, "score"))
    df_clean["recommendations"] = df_clean["recommendations"].apply(lambda x: get_nested_value(x, "total"))
    df_clean["release_date"] = df_clean["release_date"].apply(safe_extract_date)

    # Étape 4 : éclater price_overview
    price_fields = ["currency", "discount_percent", "initial_formatted", "final_formatted"]
    for field in price_fields:
        df_clean[f"price_{field}"] = df_clean["price_overview"].apply(lambda x: get_nested_value(x, field))
    df_clean.drop(columns=["price_overview"], inplace=True)

    # Étape 5 : nettoyer les langues supportées
    df_clean["supported_languages"] = df_clean["supported_languages"].apply(clean_languages)

    # Étape 6 : index = nom du jeu
    df_clean = df_clean.set_index("name")

    # Étape 7 : sauvegarde en CSV
    df_clean.to_csv("df_clean.csv")

    return df_clean 