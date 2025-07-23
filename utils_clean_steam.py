import ast
import re

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
