from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time


def scrape_products(url):
    # Initialiser le navigateur Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Mode sans interface graphique
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    all_products = []
    page = 1
    screenshot_taken = False

    while True:
        if page == 1:
            current_url = url
        else:
            current_url = f"{url}page/{page}/"

        driver.get(current_url)
        # Prendre une capture d'écran à la première page
        if not screenshot_taken:
            driver.save_screenshot('capture_selenium.png')
            print("Capture d'écran enregistrée sous 'capture_selenium.png'.")
            screenshot_taken = True
        try:
            # Attendre que les produits soient chargés
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'li.type-product'))
            )
        except:
            print(f"Aucun produit trouvé ou fin de pagination à la page {page}.")
            break

        products = driver.find_elements(By.CSS_SELECTOR, 'li.type-product')
        if not products:
            print(f"Aucun produit trouvé à la page {page}.")
            break

        for product in products:
            try:
                name = product.find_element(By.CSS_SELECTOR, 'h2.woocommerce-loop-product__title').text.strip()
                price = product.find_element(By.CSS_SELECTOR, 'span.woocommerce-Price-amount').text.strip()
                link = product.find_element(By.CSS_SELECTOR, 'a.woocommerce-LoopProduct-link').get_attribute('href')
                img = product.find_element(By.CSS_SELECTOR, 'img.attachment-woocommerce_thumbnail').get_attribute('src')
                all_products.append({
                    'name': name,
                    'price': price,
                    'link': link,
                    'image_url': img
                })
                print(f"Produit trouvé : {name}")
            except Exception as e:
                print(f"Erreur sur un produit : {e}")
                continue
        print(f"Page {page} traitée.")
        page += 1
        time.sleep(1)

    driver.quit()
    return all_products

def save_to_csv(products, filename):
    headers = ['name', 'price', 'link', 'image_url']
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(products)

def main():
    url = 'https://www.gueuledejoie.com/eshop-categorie/vins-sans-alcool/'
    print("Démarrage du scraping avec Selenium...")
    products = scrape_products(url)
    if products:
        print(f"{len(products)} produits trouvés.")
        save_to_csv(products, 'vins_sans_alcool.csv')
        print("Données enregistrées dans 'vins_sans_alcool.csv'.")
    else:
        print("Aucun produit trouvé.")

if __name__ == "__main__":
    main() 