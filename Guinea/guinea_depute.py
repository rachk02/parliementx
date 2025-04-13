import csv
import requests
from bs4 import BeautifulSoup

# Demander l'URL de la page web
url = 'https://assembleeguinee.org/les-anciens-deputes-8eme-legislature'

# Récupérer le HTML avec requests
response = requests.get(url)
response.encoding = 'utf-8'
html = response.text

# Parser le HTML
soup = BeautifulSoup(html, 'html.parser')

# Trouver le tableau
table = soup.find('table', class_='table table-bordered table-hover table-condensed')

# Extraire les en-têtes (en excluant la première colonne "N°")
headers = [th.text.strip() for th in table.find('thead').find_all('th')][1:]

# Extraire les données (en excluant la première colonne numérique)
rows = []
for tr in table.find('tbody').find_all('tr'):
    row = [td.text.strip() for td in tr.find_all('td')][1:]  # Ignorer le premier élément
    rows.append(row)

# Écrire dans un fichier CSV
with open('deputes.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(headers)
    writer.writerows(rows)

print("Fichier CSV généré avec succès !")