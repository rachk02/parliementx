import csv
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup


# Configuration du driver Chrome en mode headless
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# Remplacer par l'URL exacte de la page des sénateurs
url = "https://nass.gov.ng/mps/members"
driver.get(url)

wait = WebDriverWait(driver, 10)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_birth_date(member_url):

    # link_soup = BeautifulSoup(driver.page_source, 'html.parser')
    # link = link_soup.find('a', class_='house-green')
    link = f'https://nass.gov.ng{member_url}'
    resp = requests.get(link, headers=headers)
    resp.raise_for_status()
    birth_soup = BeautifulSoup(resp.text, 'html.parser')
    card = birth_soup.find('div', class_='list-group')
    dd = 'N/A'

    for item in card.find_all('a', class_='list-group-item list-group-item-action clearfix'):
        label = item.find('strong').get_text(strip=True)
        value = item.get_text(strip=True)

        if label == 'Date of Birth:':
            dd = value

    return dd


driver.find_element(By.NAME, "mem_length").click()
dropdown = driver.find_element(By.NAME, "mem_length")
dropdown.find_element(By.XPATH, "//option[. = '100']").click()
time.sleep(5)

csv_file = "nigeria_deputes.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["nom", "date_de_naissance", "etat", "district", "parti_politique"])

    for page in range(3):

        soup = BeautifulSoup(driver.page_source, "html.parser")
        table = soup.find("table", id="mem")
        if not table:
            print("Tableau non trouvé sur la page.")
            break

        tbody = table.find("tbody")
        if tbody:
            rows = tbody.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 4:
                    nom = cols[0].get_text(strip=True)
                    date_de_naissance = get_birth_date(cols[0].find("a").get("href"))
                    etat = cols[1].get_text(strip=True)
                    district = cols[2].get_text(strip=True)
                    parti_politique = cols[3].get_text(strip=True)
                    writer.writerow([nom, date_de_naissance, etat, district, parti_politique])
                    print(f"Données sauvegardées pour : {nom}")
        else:
            print("Aucun tbody trouvé dans le tableau.")

        # Gestion du clic sur le bouton "Next"
        try:
            next_button = driver.find_element(By.LINK_TEXT, "Next")
            next_button.click()
            print(f"Passage à la page {page + 2}")
            time.sleep(10)
        except Exception as e:
            print("Erreur lors du clic sur Next :", e)
            break

driver.quit()
print(f"Scraping terminé. Les données ont été enregistrées dans {csv_file}.")
