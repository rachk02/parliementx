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
url = "https://sapl.parlamento.gw/parlamentar/"
driver.get(url)
time.sleep(20)
soup = BeautifulSoup(driver.page_source, 'html.parser')

deputes = []

# Trouver la table
table = soup.find('table', class_='table table-striped table-hover table-link-ordering')

# Itérer sur chaque ligne du tableau
for row in table.find_all('tbody'):
    for tr in row.find_all('tr'):
        cols = tr.find_all('th')

        nom_tag = cols[0].find('a')
        nom = nom_tag.text.strip() if nom_tag else 'N/A'

        parti = cols[1].get_text(strip=True)
        actif = cols[2].find('p').get_text(strip=True)
        titulaire = cols[3].find('p').get_text(strip=True)

        deputes.append({
            'Nom': nom,
            'Parti': parti,
            'Actif': actif,
            'Titulaire': titulaire
        })

# Créer le fichier CSV
filename = 'deputes.csv'
with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
    fieldnames = ['Nom', 'Parti', 'Actif', 'Titulaire']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')

    writer.writeheader()
    for depute in deputes:
        writer.writerow(depute)

print(f"Fichier CSV '{filename}' créé avec {len(deputes)} entrées")