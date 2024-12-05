import classNewsApi as news
from dotenv import load_dotenv
import os
import json
import requests
from bs4 import BeautifulSoup
import pickle
import pandas as pd

##### CREATION D'ARTICLES #####

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement
api_key = os.getenv("NEWSAPI_KEY")

# Créer une instance de la classe NewsAPIClient
news_client = news.NewsAPIClient(api_key)

# Rechercher d'articles sur le thème "intelligence artificielle"
articles = news_client.search_news("intelligence artificielle", page_size=10)

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


### Data frame
dfArticles = pd.DataFrame(articles)

# afficher colonnes
print(dfArticles.columns)

# affocher la collone 'full_content'
print(dfArticles['full_content'])


##### SAUVEGARDE D'ARTICLES #####

## Save 
with open("articles.pkl", "wb") as f:
    pickle.dump(dfArticles, f)

# Open  
with open("articles.pkl", "rb") as f:
    articlesPickel = pickle.load(f)

print("Les articles avec leur contenu complet ont été sauvegardés dans 'articles.pkl'.")

# Nombre de mots et de phrases dans chaque article
for index, row in articlesPickel.iterrows():
    contenu = row['full_content'] 
    mots = contenu.split()
    phrases = contenu.split('.')
    print(f"Article {index + 1}:")
    print(f"Nombre de mots : {len(mots)}")
    print(f"Nombre de phrases : {len(phrases)}")
    print()
