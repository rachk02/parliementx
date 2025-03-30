import csv
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Configuration du driver Chrome
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Décommenter pour le mode headless
options.add_argument("--start-maximized")  # Pour éviter les problèmes de visibilité
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# Configuration
url = "https://assemblee-nationale.tg/deputes/"
csv_file = 'togo_deputes.csv'


def parse_page(page_source):
    """Extrait les données de la page"""
    soup = BeautifulSoup(page_source, 'html.parser')
    members = soup.select('div.e-con-full.e-con')  # Sélecteur ajusté

    data = []
    for member in members:
        try:
            # Nom
            name_tag = member.select_one('h1.elementor-heading-title')
            nom = name_tag.get_text(strip=True) if name_tag else 'N/A'

            # Région et Parti
            h2_tags = member.select('h2.elementor-heading-title')
            region = h2_tags[0].text.strip() if len(h2_tags) > 0 else 'N/A'
            parti = h2_tags[1].text.strip() if len(h2_tags) > 1 else 'N/A'

            data.append({
                'nom': nom,
                'region': region,
                'parti': parti
            })

        except Exception as e:
            print(f"Erreur d'extraction : {str(e)}")

    return data


def save_to_csv(data):
    """Sauvegarde les données en CSV"""
    with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['nom', 'region', 'parti'])
        writer.writeheader()
        writer.writerows(data)
    print(f"{len(data)} entrées sauvegardées dans {csv_file}")


# Exécution principale
try:
    driver.get(url)
    time.sleep(60)

    # Attendre le chargement des éléments
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.e-con-full.e-con'))
    )

    # Pause supplémentaire pour le chargement dynamique
    time.sleep(2)

    # Extraction des données
    data = parse_page(driver.page_source)

    # Sauvegarde
    if data:
        save_to_csv(data)
    else:
        print("Aucune donnée trouvée")

finally:
    driver.quit()