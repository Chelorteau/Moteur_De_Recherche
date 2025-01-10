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
import numpy as np

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

## AFFICHAGE AVEC STREAMLIT ##
# lancer streamlit run .\main.py

search_engine = SearchEngine(SourceWithName)

# Titre de l'application
st.title("Moteur de recherche sur l'intelligence artificielle")

## STATS  GLOBAL ##
    
st.sidebar.title("STATISTIQUES")

st.sidebar.subheader("Statistiques globales")
st.sidebar.markdown(f"**Total de documents** : {len(search_engine.documents)}")
st.sidebar.markdown(f"**Taille du vocabulaire** : {len(search_engine.vocab)}")

# Saisie des mots-clés par l'utilisateur
query = st.text_input("Entrez les mots-clés à rechercher :", "")

# Vérifier si une requête est saisie
if query:
    # Effectuer une recherche
    _, total_docs = search_engine.search(query, nb_doc=1)

    # Barre de défilement pour le nombre de documents à retourner
    x = st.slider(
        "Nombre de documents à afficher :",
        min_value=1,
        max_value=total_docs,
        value=3,
        step=1,
        format="%d"
    )
    # Afficher les résultats
    resultats, _ = search_engine.search(query, nb_doc=x)
    st.subheader(f"Résultats pour : '{query}'")
    if resultats:
        for doc, score in resultats:
            st.markdown(f"### {doc.titre}")
            st.markdown(f"- **Score** : {score:.4f}")
            st.markdown(f"- [Lire l'article]({doc.url})")
            st.markdown("---")
    else:
        st.write("Aucun résultat trouvé.")


    ## STATS ##

    st.sidebar.subheader(f"Statistiques pour '{query}'")
    word_stats = search_engine.get_word_stats(query)  

    if word_stats:
        st.sidebar.markdown(f"- **Occurrences totales** : {word_stats['occurrences']}")
        st.sidebar.markdown(f"- **Documents contenant ce mot** : {word_stats['document_frequency']}")
    else:
        st.sidebar.write("Aucune statistique disponible pour ce mot.")

    # Top mots fréquents
    st.sidebar.subheader("Top 5 des mots fréquents")
    top_words = sorted(search_engine.vocab.items(), key=lambda x: x[1]['occurrences'], reverse=True)[:5]
    for word, info in top_words:
        st.sidebar.markdown(f"- {word} : {info['occurrences']} occurrences")




    



