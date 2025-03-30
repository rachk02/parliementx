import requests
from bs4 import BeautifulSoup
import csv

# Configuration des en-têtes pour éviter le blocage
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

url = "https://www.parliament.gov.sl/members-of-parliament.html"

try:
    # Requête HTTP avec gestion d'erreur
    response = requests.get(url, headers=headers, timeout=15)
    response.raise_for_status()
except Exception as e:
    print(f"Erreur de connexion : {str(e)}")
    exit()

# Utilisation du parser HTML intégré
soup = BeautifulSoup(response.content, 'html.parser')

# Récupération des membres
members = soup.select('ul.memberboxes > li.wow.fadeIn')

if not members:
    print("Aucun membre trouvé - Vérifiez la structure HTML")
    exit()

# Liste des partis connus (à adapter selon les besoins)
known_parties = {'SLPP', 'APC', 'NGC', 'C4C', 'PMDC', 'PDM'}

donnees = []

for membre in members:
    # Extraction du nom
    nom_tag = membre.select_one('.profileName a')
    nom = nom_tag.get_text(strip=True) if nom_tag else 'Nom inconnu'

    # Initialisation des données
    infos = {
        'Nom': nom,
        'District': '',
        'Région': '',
        'Partis': [],
        'Fonctions': []
    }

    # Extraction des détails
    details = membre.select('.profileDesc li:not(:has(script))')

    for detail in details:
        texte = detail.get_text(strip=True)

        # Détection intelligente des informations
        if 'District' in texte:
            infos['District'] = texte.replace('District', '').strip()
        elif 'Region' in texte:
            infos['Région'] = texte.replace('Region', '').strip()
        elif texte in known_parties:
            infos['Partis'].append(texte)
        else:
            infos['Fonctions'].append(texte)

    # Formatage final
    infos['Partis'] = '|'.join(infos['Partis']) or 'Indépendant'
    infos['Fonctions'] = '|'.join(infos['Fonctions']) or 'Membre du Parlement'

    donnees.append(infos)

# Création du fichier CSV
if donnees:
    with open('membres_parlement.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=donnees[0].keys())
        writer.writeheader()
        writer.writerows(donnees)
    print(f"✅ {len(donnees)} membres enregistrés avec succès")
else:
    print("Aucune donnée à exporter")