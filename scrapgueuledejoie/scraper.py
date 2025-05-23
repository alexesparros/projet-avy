import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# 1. Récupérer toutes les URLs de produits sur la page catégorie
def get_product_urls(category_url):
    urls = []
    page = 1
    while True:
        if page == 1:
            url = category_url
        else:
            url = f"{category_url}?page={page}"
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        with open(f"page_{page}.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())
        links = soup.select('a[href^="/collections/vins-sans-alcool/products/"]')
        if not links:
            break
        for a in links:
            href = a.get("href")
            full_url = "https://www.sanzalc.com" + href
            if full_url not in urls:
                urls.append(full_url)
        page += 1
        time.sleep(1)
    return urls

# 2. Scraper les infos de chaque fiche produit
def extract_product_data(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    try:
        name = soup.select_one("h1.t4s-product__title").get_text(strip=True)
    except:
        name = ""
    try:
        price = soup.select_one(".price .price-item--regular").get_text(strip=True)
    except:
        price = ""
    try:
        image = soup.select_one("img.t4s-product__media-img")["src"]
        if image.startswith("//"):
            image = "https:" + image
    except:
        image = ""
    try:
        desc = soup.select_one(".t4s-product__description").get_text(" ", strip=True)
    except:
        desc = ""
    try:
        producer = soup.select_one(".product__vendor").get_text(strip=True)
    except:
        producer = ""
    return {
        "Nom": name,
        "Producteur": producer,
        "Lien produit": url,
        "Image": image,
        "Prix": price,
        "Description": desc
    }

# 3. Utilisation
category_url = "https://www.sanzalc.com/collections/vins-sans-alcool"
print("Récupération des URLs produits...")
urls = get_product_urls(category_url)
print(f"{len(urls)} produits trouvés.")

data = []
for url in urls:
    print(f"Scraping: {url}")
    data.append(extract_product_data(url))
    time.sleep(1)

df = pd.DataFrame(data)
df.to_csv("sanzalc_vins_sans_alcool.csv", index=False, encoding="utf-8-sig")
print("✅ Export CSV terminé ! Fichier : sanzalc_vins_sans_alcool.csv")