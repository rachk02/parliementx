from bs4 import BeautifulSoup
import requests
import time


def get_all_member_links():

    base_url = "https://www.parliament.gh/members"
    all_hrefs = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for page in range(1, 8):  # Pages 1 à 7
        # Construire l'URL de la page
        if page == 1:
            url = base_url
        else:
            url = f"{base_url}?page={page}"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            member_links = soup.find_all('a', {'class': 'col-10', 'style': 'height: 100%;'})

            # Ajouter les hrefs à la liste globale
            for link in member_links:
                all_hrefs.append(link.get('href'))

            print(f"Page {page} traitée avec succès | {len(member_links)} liens trouvés")
            time.sleep(2)  # Respect des bonnes pratiques

        except Exception as e:
            print(f"Erreur sur la page {page} : {str(e)}")

    # Résultats finaux
    print(f"\nTotal de liens récupérés : {len(all_hrefs)}")
    print("Exemple de liens :")
    print(all_hrefs[:5])  # Affiche les 5 premiers liens
    return all_hrefs