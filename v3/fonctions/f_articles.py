#### CLASS IMPORTER ####
import requests
from bs4 import BeautifulSoup

# Fonction pour récupérer le contenu complet d'un article via son URL
def get_full_content(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            full_content = " ".join([p.get_text() for p in paragraphs])
            return full_content
        else:
            return "Impossible de récupérer le contenu. Erreur HTTP."
    except Exception as e:
        return f"Erreur lors de la récupération du contenu : {e}"