import json
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import glob

products = []

# Parcourir toutes les pages sauvegardées
for page_file in sorted(glob.glob("page_*.html")):
    print(f"Traitement de {page_file} ...")
    with open(page_file, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        try:
            data = json.loads(script.string)
            if isinstance(data, dict) and "itemListElement" in data:
                for item in data["itemListElement"]:
                    name = item.get("name", "")
                    # Chercher le prix dans la page catégorie
                    price = ""
                    price_divs = soup.find_all("div", class_="t4s-product-price")
                    found = False
                    for div in price_divs:
                        parent = div.find_parent()
                        if parent and name in parent.text:
                            price = div.text.strip()
                            found = True
                            break
                    if not found and price_divs:
                        for div in price_divs:
                            if div.text.strip():
                                price = div.text.strip()
                                break
                    prod = {
                        "Nom": name,
                        "Description": item.get("description", ""),
                        "Image": "https:" + item.get("image", "") if item.get("image", "").startswith("//") else item.get("image", ""),
                        "URL": "https://" + item.get("url", "") if item.get("url", "").startswith("www.") else item.get("url", ""),
                        "Prix": price
                    }
                    products.append(prod)
        except Exception as e:
            continue

def extract_complementary_info(product_url):
    try:
        resp = requests.get(product_url)
        soup = BeautifulSoup(resp.text, "html.parser")
        tab_titles = soup.find_all("a", class_="t4s-tab__title")
        info_id = None
        for tab in tab_titles:
            if "INFORMATIONS COMPLÉMENTAIRES" in tab.get_text(strip=True).upper():
                info_id = tab.get("href", "").replace("#", "")
                break
        info_text = ""
        if info_id:
            info_div = soup.find(id=info_id)
            if info_div:
                info_text = info_div.get_text(" ", strip=True)
        return info_text
    except Exception as e:
        return ""

print("Extraction des informations complémentaires pour chaque produit...")
for i, prod in enumerate(products):
    url = prod["URL"]
    prod["Informations complémentaires"] = extract_complementary_info(url)
    print(f"{i+1}/{len(products)} OK : {prod['Nom']}")
    time.sleep(1)

# Exporter en CSV
if products:
    df = pd.DataFrame(products)
    df.to_csv("sanzalc_produits_jsonld.csv", index=False, encoding="utf-8-sig")
    print("✅ Export CSV avec infos complémentaires terminé ! Fichier : sanzalc_produits_jsonld.csv")
else:
    print("Aucun produit trouvé dans le JSON-LD.") 