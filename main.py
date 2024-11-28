import classNewsApi as news
from dotenv import load_dotenv
import os
import json

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer la clé API depuis les variables d'environnement
api_key = os.getenv("NEWSAPI_KEY")

# Créer une instance de la classe NewsAPIClient
news_client = news.NewsAPIClient(api_key)

# Rechercher des articles sur le thème "intelligence artificielle"
articles = news_client.search_news("intelligence artificielle", page_size=5)

# Afficher les articles
print(json.dumps(articles, indent=4, ensure_ascii=False))

