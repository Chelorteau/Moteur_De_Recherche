import classNewsApi as news
from dotenv import load_dotenv
import os
import json
import pickle

##### CREATION D'ARTICLES #####

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement
api_key = os.getenv("NEWSAPI_KEY")

# Créer une instance de la classe NewsAPIClient
news_client = news.NewsAPIClient(api_key)

# Rechercher  d'articles sur le thème "intelligence artificielle"
articles = news_client.search_news("intelligence artificielle", page_size=100)

##### RECUPERATION DU CONTENU COMPLET #####

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
    
# Ajouter le contenu complet à chaque article
for article in articles:
    url = article.get('url')
    if url:
        article['full_content'] = get_full_content(url)
    else:
        article['full_content'] = "URL non disponible."

##### SAUVEGARDE D'ARTICLES #####

# Enregistrer les articles dans un fichier pickle
with open("articles.pkl", "wb") as f:
   pickle.dump(articles, f)

# Charger les articles depuis le fichier pickle
with open("articles.pkl", "rb") as f:
   articles = pickle.load(f)

##### MANIPULATION D'ARTICLES #####

# Pour chaque document, affichez le nombre de mots et de phrases. Pour cela, vous utiliserez la onction split 

# nb de mots et de phrases
for article in articles:
    contenu = article['content']
    mots = contenu.split()
    phrases = contenu.split('.')
    print(f"Nombre de mots : {len(mots)}")
    print(f"Nombre de phrases : {len(phrases)}")
    print()