import csv
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Configuration du driver Chrome
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Pour éviter les problèmes de visibilité
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://assemblee-nationale.bj/index.php/depute/menu-liste-des-deputes/liste-des-deputes/"
driver.get(url)

wait = WebDriverWait(driver, 15)

# Sélectionner 100 éléments par page
dropdown = wait.until(EC.element_to_be_clickable((By.NAME, "tablepress-1_length")))
dropdown.find_element(By.XPATH, "//option[. = '100']").click()
time.sleep(2)  # Attente courte après sélection

headers = ["nom", "parti_politique"]
all_deputes = []

while True:
    # Attendre le chargement du tableau
    wait.until(EC.presence_of_element_located((By.ID, "tablepress-1")))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table', {'id': 'tablepress-1'})

    for row in table.find('tbody').find_all('tr'):
        cols = row.find_all('td')
        nom = cols[0].get_text(strip=True)
        parti = cols[1].get_text(strip=True)
        all_deputes.append([nom, parti])

    # Gestion de la pagination avec vérification explicite
    next_button = driver.find_element(By.ID, "tablepress-1_next")

    if "disabled" in next_button.get_attribute("class"):
        break
    else:
        # Faire défiler jusqu'au bouton avant de cliquer
        driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(2)  # Attendre le chargement de la nouvelle page

# Écrire les résultats dans le CSV
with open('deputes.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(all_deputes)

print(f"{len(all_deputes)} députés sauvegardés dans deputes.csv")
driver.quit()