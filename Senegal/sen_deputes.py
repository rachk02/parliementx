import csv
import time
from selenium.webdriver.chrome.service import Service
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

# Configuration
url = "https://www.vie-publique.sn/elections/legislatives/resultats/deputes"
driver.get(url)
time.sleep(5)

try:
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Trouver le conteneur principal
    container = soup.find('div', class_='grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4')

    if not container:
        raise Exception("Conteneur des députés introuvable")

    # Extraire toutes les cartes de députés
    cards = container.find_all('div', class_='relative flex h-56 flex-col overflow-hidden rounded-lg shadow-lg')

    data = []

    for card in cards:
        try:
            # Extraction des éléments
            img = card.find('img')

            # Récupération du nom depuis l'attribut alt de l'image
            nom_complet = img['alt'].strip().title() if img and img.has_attr('alt') else 'N/A'
            nom_complet = ' '.join(nom_complet.split())  # Normalisation des espaces

            details_element = card.find('p', class_='mb-1')
            parti_element = card.find(lambda tag: tag.name == 'h4' and 'style' in tag.attrs)

            # Traitement des données
            details = details_element.get_text(strip=True) if details_element else ''
            age_profession = details.split('|') if details else ['', '']

            # Nettoyage supplémentaire
            age = age_profession[0].replace('ans', '').strip() if len(age_profession) > 0 else ''
            profession = age_profession[1].strip() if len(age_profession) > 1 else ''

            # Extraction de la couleur
            style = parti_element['style'] if parti_element else ''
            couleur = style.split(':')[-1].strip('; ') if style else ''

            data.append({
                'Nom': nom_complet,
                'Age': age,
                'Profession': profession,
                'Parti': parti_element.get_text(strip=True) if parti_element else 'N/A',
                'Couleur': couleur,
                'Photo': img['src'].replace('&amp;', '&') if img else ''
            })

        except Exception as e:
            print(f"Erreur sur une carte: {str(e)}")
            continue

    # Export CSV
    with open('deputes.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['Nom', 'Age', 'Profession', 'Parti', 'Couleur', 'Photo'])
        writer.writeheader()
        writer.writerows(data)

    print(f"Export réussi: {len(data)} députés trouvés")

except Exception as e:
    print(f"Erreur générale: {str(e)}")

finally:
    driver.quit()  # Fermeture propre du navigateur