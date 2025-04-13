import csv
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from bs4 import BeautifulSoup

# Configuration du driver Chrome
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Décommenter pour le mode headless
options.add_argument("--start-maximized")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# URL cible
url = "https://www.parlamento.cv/deputados_ef.php"
driver.get(url)
time.sleep(5)

# Création du fichier CSV
with open('deputes.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Nom', 'Circonscription', 'Parti', 'Photo URL'])

    page_count = 1

    while page_count <= 5:
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        membres = soup.find_all('div', class_='row ng-scope')

        for membre in membres:
            try:
                # Photo
                img = membre.find('img', class_='thumbnail')
                photo_url = img['src'] if img else ""

                # Initialisation
                nom = circonscription = parti = ""

                infos = membre.find_all('div', class_='col-xs-12 col-lg-4')

                for info in infos:
                    titre_div = info.find('div', class_='TextoRegular-Titulo')
                    if not titre_div:
                        continue
                    titre = titre_div.get_text(strip=True)

                    if 'Nome' in titre:
                        nom_tag = info.find('a')
                        nom = nom_tag.get_text(strip=True) if nom_tag else ""
                    elif 'Círculo Eleitoral' in titre:
                        circ_span = info.find('span')
                        circonscription = circ_span.get_text(strip=True) if circ_span else ""
                    elif 'Grupo Parlamentar' in titre:
                        parti_span = info.find('span')
                        parti = parti_span.get_text(strip=True) if parti_span else ""

                writer.writerow([nom, circonscription, parti, photo_url])

            except Exception as e:
                print(f"Erreur lors de l'extraction: {e}")
                continue

        # Passage à la page suivante
        try:
            next_button = driver.find_element(By.PARTIAL_LINK_TEXT, '›')
            next_button.click()
            time.sleep(3)
            page_count += 1
        except NoSuchElementException:
            print("Fin des pages")
            break
        except Exception as e:
            print(f"Erreur de navigation: {e}")
            break

driver.quit()
