#### CLASS LOCAL ####
import Class.classNewsApi as news
import Class.Document as doc
import Class.Source as source
import Class.DocumentFactory as DF
from Class.search_engine import SearchEngine

#### FONCTION LOCAL ####
from fonctions.f_articles import get_full_content
#### CLASS IMPORTER ####
from dotenv import load_dotenv
import os

import pickle
import pandas as pd
import streamlit as st


######|| MOTEUR DE RECHERCHE SUR L'INTELLIGENCE ARTIFICIELLE ||######


##### 1 . RECUPERATION D'ARTICLES #####

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

#  si articles.pkl n'existe pas 
if not os.path.exists("articles.pkl"):
    # Récupérer la clé API depuis les variables d'environnement
    api_key = os.getenv("NEWSAPI_KEY")

    # Créer une instance de la classe NewsAPIClient
    news_client = news.NewsAPIClient(api_key)

    # Rechercher d'articles sur le thème "intelligence artificielle"
    articles = news_client.search_news("intelligence artificielle", page_size=100)

## 1.1 RECUPERATION DU CONTENU COMPLET DES ARTICLES ##
    # Ajouter le contenu complet à chaque article
    for article in articles:
        url = article.get('url')
        if url:
            article['full_content'] = get_full_content(url)
        else:
            article['full_content'] = "URL non disponible."

## 1.2 SAUVEGARDE DES ARTICLES ##

    # créer un DataFrame à partir de la liste d'articles
    dfArticles = pd.DataFrame(articles)

    # Enregistrer les articles dans un fichier pickle
    ## Save 
    with open("articles.pkl", "wb") as f:
        pickle.dump(dfArticles, f)

## 1.3 CHARGEMENT DES ARTICLES ##

# Charger les articles depuis le fichier pickle
with open("articles.pkl", "rb") as f:
    articlesPickel = pickle.load(f)

##### 2 . CREATION DE DOCUMENTS et de SOURCE  #####

# Créer une collection de documents à partir des articles
CollectionWithID = {}

# Créer une collection de Sources à partir des articles
SourceWithName = {}

for index, row in articlesPickel.iterrows():
    # Créer un objet Document
    document = DF.DocumentFactory.create_document(row)
    # Ajouter le document à la collection
    CollectionWithID[index] = document

    # Gérer les sources
    source_name = row['source']['name'] if isinstance(row['source'], dict) else "Source inconnue"

    # Vérifier si la source existe déjà dans SourceWithID
    if source_name not in SourceWithName:
        # Créer une nouvelle Source si elle n'existe pas
        SourceWithName[source_name] = source.Source(source_name)
    
    # Ajouter le document à la production de la source
    SourceWithName[source_name].add(document, index)

# Sauvegarder SourceWithName 
with open("sources.pkl", "wb") as f:
    pickle.dump(SourceWithName, f)

# supprimer les variables inutiles
del SourceWithName
# Charger SourceWithName
with open("sources.pkl", "rb") as f:
    SourceWithName = pickle.load(f)

# STATISTIQUES DES SOURCES #

print("### STATISTIQUES DES SOURCES ###\n")

for source_name, source_obj in SourceWithName.items():
    n = 10
    print(source_obj)
    print("-" * 50)
    print("Statistiques des documents:\n")
    stats = source_obj.stats(n) 
    print(f"Vocabulaire unique: {len(stats['vocabulaire'])} mots")
    print(f"Les {n} mots les plus fréquents:")

    print(stats['freq_table'].to_string(index=False)) 
    
    print("\n" + "=" * 80 + "\n")


# MOTEUR DE RECHERCHE

# Initialisation avec SourceWithName
search_engine = SearchEngine(SourceWithName)

# Effectuer une recherche
# Ex : Recherche pour "IA"
resultats = search_engine.search("IA", nb_doc=6)

# Afficher les résultats
print(f"Résultats de la recherche pour 'IA' :")
for doc, score in resultats:
    print(f"Titre : {doc.titre}")
    print(f"Score : {score:.4f}")
    print(f"URL : {doc.url}")
    print("---")





