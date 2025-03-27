import csv
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
import time
from ghana_parliement_links import get_all_member_links

# Configuration de base
base_url = "https://www.parliament.gh/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Liste des URLs des membres (à remplacer par votre liste récupérée précédemment)
member_hrefs = get_all_member_links()

# Préparation du CSV
with open('parlement_ghana.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=[
        'nom',
        'sexe',
        'date_de_naissance',
        'region',
        'ethnie',
        'langue',
        'religion',
        'parti_politique'
    ])
    writer.writeheader()

    for href in member_hrefs:
        member_url = urljoin(base_url, href)

        try:
            # Récupération de la page
            response = requests.get(member_url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            card = soup.find('div', class_='card text-center row gloss')

            if not card:
                continue

            # Extraction des données
            data = {
                'nom': card.find('h1').get_text(strip=True) if card.find('h1') else 'N/A',
                'sexe': 'N/A',
                'date_de_naissance': 'N/A',
                'region': 'N/A',
                'ethnie': 'N/A',
                'langue': 'N/A',
                'religion': 'N/A',
                'parti_politique': 'N/A'
            }

            # Extraction des détails
            for item in card.find_all('li', class_='list-group-item'):
                label = item.find('div', class_='col-4').get_text(strip=True)
                value = item.find('div', class_='col-8').get_text(strip=True)

                if label == 'Hometown':
                    data['region'] = value
                elif label == 'Date of Birth':
                    data['date_de_naissance'] = value
                elif label == 'Religion':
                    data['religion'] = value
                elif label == 'Political Party':
                    data['parti_politique'] = value

            writer.writerow(data)
            print(f"Données sauvegardées pour : {data['nom']}")
            time.sleep(1.5)

        except Exception as e:
            print(f"Erreur avec {member_url} : {str(e)}")
            continue

print("Scraping terminé ! Fichier CSV généré.")