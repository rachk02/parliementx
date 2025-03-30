import requests
from bs4 import BeautifulSoup
import csv

# Récupération du contenu HTML
url = "https://www.assembleenationale.bf/depute/depute#"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Trouver le conteneur principal
container = soup.find('div', class_='grid grid-cols-2 md:grid-cols-5 gap-6')

noms = []

if container:
    for personne in container.find_all('div', class_='flex flex-col items-center'):
        nom_tag = personne.find('strong')
        if nom_tag:
            nom = nom_tag.get_text(strip=True)
            noms.append(nom)

# Enregistrement en CSV
with open('noms.csv', 'w', newline='', encoding='utf-8') as fichier_csv:
    writer = csv.writer(fichier_csv)

    # Écrire l'en-tête
    writer.writerow(['Nom'])

    # Écrire les données
    for nom in noms:
        writer.writerow([nom])

print("Fichier CSV créé avec succès !")