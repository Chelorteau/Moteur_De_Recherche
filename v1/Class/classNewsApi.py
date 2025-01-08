import requests
class NewsAPIClient:
    def __init__(self, api_key, base_url='https://newsapi.org/v2/everything', language='fr'):
        """
        Initialise le client NewsAPI.
        
        :param api_key: La clé API de NewsAPI.
        :param base_url: URL de base de l'API (par défaut : 'https://newsapi.org/v2/everything').
        :param language: Langue des articles (par défaut : 'fr' pour le français).
        """
        self.api_key = api_key
        self.base_url = base_url
        self.language = language
        
        # Vérifie si la clé API est fournie
        if not self.api_key:
            raise ValueError("La clé API NewsAPI n'est pas fournie.")

    def search_news(self, theme, page_size):
        """
        Recherche des articles sur un thème spécifique.
        
        :param theme: Le thème ou mot-clé pour la recherche.
        :param page_size: Nombre d'articles par page
        :return: Json Liste d'articles.
        """
        params = {
            'q': theme,               
            'pageSize': page_size,  
            'apiKey': self.api_key,  
            'language': self.language
        }

        response = requests.get(self.base_url, params=params)

        # Vérification de la réponse de l'API
        if response.status_code == 200:
            articles = response.json().get('articles', [])
            return articles
        else:
            print("Erreur:", response.status_code, response.text)
            return None
