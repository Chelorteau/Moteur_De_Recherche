import re
import pandas as pd
from collections import defaultdict

class Source:
    def __init__(self, name, ndoc=0, production=None):
        """
        Initialise une instance de la classe Source.

        :param name: Nom de la source (str)
        :param ndoc: Nombre de documents associés à cette source (int, par défaut 0)
        :param production: Dictionnaire associant un ID à un document (dict, par défaut vide)
        """
        self.name = name
        self.ndoc = ndoc
        self.production = production if production is not None else {}

    def add(self, document, doc_id):
        """
        Ajoute un document à la production de la source.

        :param document: Document à ajouter
        :param doc_id: Identifiant unique du document
        """
        self.production[doc_id] = document
        self.ndoc += 1

    def __str__(self):
        """
        Retourne une représentation textuelle de la source.

        :return: Une chaîne décrivant la source et le nombre de documents associés
        """
        return (
            f"Source : {self.name}\n"
            f"Nombre de documents : {self.ndoc}\n"
            f"Documents disponibles : {', '.join(map(str, self.production.keys())) if self.production else 'Aucun document.'}"
        )

    def search(self, keyword):
        """
        Recherche les passages contenant le mot-clé dans tous les documents des Sources.

        :param keyword: Mot-clé à rechercher
        :return: Liste des passages contenant le mot-clé
        """
        # Concaténer tous les contenus des documents la première fois
        if self._concatenated_content is None:
            self._concatenated_content = " ".join(
                doc.full_content for doc in self.production.values() if doc.full_content
            )

        # Rechercher les passages contenant le mot-clé
        matches = re.finditer(rf"(.{{0,20}}{re.escape(keyword)}.{{0,20}})", self._concatenated_content, re.IGNORECASE)
        
        # Retourner les passages trouvés
        return [match.group(0) for match in matches]
    
    def concorde(self, expression, context_size=30):
        """
        Construit un concordancier pour une expression donnée.

        :param expression: Expression régulière à rechercher (str)
        :param context_size: Taille du contexte gauche et droit (int)
        :return: DataFrame avec les colonnes 'contexte gauche', 'motif trouvé', 'contexte droit'
        """
        # Construire le contenu concaténé si ce n'est pas déjà fait
        if self._concatenated_content is None:
            self._concatenated_content = " ".join(
                doc.full_content for doc in self.production.values() if doc.full_content
            )
        
        # Expression régulière pour capturer le motif avec le contexte
        pattern = re.compile(rf"(.{{0,{context_size}}})({expression})(.{{0,{context_size}}})", re.IGNORECASE)
        matches = pattern.findall(self._concatenated_content)
        
        # Construire un DataFrame à partir des résultats
        df = pd.DataFrame(matches, columns=["contexte gauche", "motif trouvé", "contexte droit"])
        return df
    
    def nettoyer_texte(self, texte):
        """
        Nettoie une chaîne de caractères en supprimant les stop words et en appliquant des transformations :
        - Convertit le texte en minuscules.
        - Remplace les passages à la ligne par des espaces.
        - Supprime les ponctuations et les chiffres.
        - Supprime les caractères spéciaux.
        - Supprime les mots présents dans une liste de stop words.

        :param texte: Chaîne de caractères à nettoyer.
        :return: Texte nettoyé sans stop words.
        """
        # Liste des stop words en français
        stop_words_fr = [
            'a', 'alors', 'ans', 'après', 'au', 'aucun', 'auquel', 'aussi', 'autre', 'autres', 'aux', 
            'auxquels', 'avant', 'avec', 'avoir', 'b', 'bon', 'c', 'car', 'ce', 'cela', 'ces', 'cet', 
            'cette', 'ceux', 'chaque', 'chez', 'ci', 'comme', 'comment', 'contre', 'd', 'dans', 'de', 
            'dedans', 'dehors', 'depuis', 'des', 'desquels', 'deux', 'devrait', 'dit', 'doit', 'donc', 
            'dont', 'dos', 'droite', 'du', 'duquel', 'début', 'e', 'elle', 'elles', 'en', 'encore', 
            'entre', 'essai', 'est', 'et', 'eu', 'f', 'fait', 'faites', 'faut', 'fois', 'font', 'force', 
            'g', 'h', 'haut', 'hors', 'i', 'ici', 'il', 'ils', 'j', 'je', 'jour', 'juste', 'k', 'l', 
            'la', 'laquelle', 'le', 'lequel', 'les', 'lesquelles', 'lesquels', 'leur', 'leurs', 'là', 
            'm', 'ma', 'maintenant', 'mais', 'mes', 'mien', 'moins', 'mon', 'mot', 'même', 'n', 'ne', 
            'ni', 'nom', 'nommés', 'non', 'nos', 'notre', 'nous', 'nouveau', 'nouveaux', 'o', 'ont', 
            'ou', 'où', 'p', 'par', 'parce', 'parole', 'pas', 'pendant', 'personnes', 'peu', 'peut', 
            'pièce', 'plupart', 'plus', 'pour', 'pourquoi', 'q', 'quand', 'que', 'quel', 'quelle', 
            'quelles', 'quels', 'qui', 'r', 's', 'sa', 'sans', 'ses', 'seulement', 'si', 'sien', 'son', 
            'sont', 'sous', 'soyez', 'sujet', 'sur', 't', 'ta', 'tandis', 'tellement', 'tels', 'tes', 
            'ton', 'tous', 'tout', 'trois', 'trop', 'très', 'tu', 'u', 'un', 'une', 'v', 'vient', 
            'voient', 'vont', 'vos', 'votre', 'vous', 'vu', 'w', 'x', 'y', 'z', 'à', 'ça', 'étaient', 
            'était', 'étant', 'état', 'étions', 'été', 'être',"cest","se","nest"
        ]


        # Conversion en minuscules
        texte = texte.lower()

        # Remplacement des passages à la ligne par des espaces
        texte = texte.replace("\n", " ")

        # Suppression des ponctuations et des chiffres
        texte = re.sub(r'[^\w\s]', '', texte)  
        texte = re.sub(r'\d+', '', texte) 

        # Suppression des caractères spéciaux
        texte = texte.encode("ascii", "ignore").decode("utf-8") 

        # Suppression des stop words
        mots_filtres = [mot for mot in texte.split() if mot not in stop_words_fr]

        # Recontitution du texte nettoyé
        texte_nettoye = " ".join(mots_filtres)

        return texte_nettoye


    def stats(self, n=10):
        """
        Calcule et retourne les statistiques textuelles sur les documents de la source :
        - Nombre de mots différents.
        - Les n mots les plus fréquents.
        - Tableau freq avec term frequency et document frequency.

        :param n: Nombre de mots les plus fréquents à afficher.
        :return: Un dictionnaire contenant les statistiques textuelles.
        """
        vocabulaire = set()  # Pour stocker les mots uniques
        freq_totale = defaultdict(int)  # Pour stocker les fréquences totales
        freq_documents = defaultdict(int)  # Pour stocker les fréquences par document

        # Parcourir les documents pour construire le vocabulaire et compter les occurrences
        for _, doc in self.production.items():
            texte_nettoye = self.nettoyer_texte(doc.full_content)
            mots = texte_nettoye.split()
            
            # Ajouter les mots au vocabulaire et compter les occurrences
            mots_uniques = set(mots)
            vocabulaire.update(mots_uniques)
            
            # Compter les occurrences
            for mot in mots:
                freq_totale[mot] += 1
            for mot in mots_uniques:
                freq_documents[mot] += 1

        # Trier le vocabulaire pour attribuer des identifiants uniques
        vocabulaire = sorted(vocabulaire)
        vocab = {
            mot: {
                "id": idx,
                "occurrences": freq_totale[mot],
                "document_frequency": freq_documents[mot],
                "length": len(mot)  
            }
            for idx, mot in enumerate(vocabulaire)
        }

        # Construire un DataFrame
        freq = pd.DataFrame({
            "mots": list(freq_totale.keys()),
            "term_frequency": list(freq_totale.values()),
            "document_frequency": [freq_documents[mot] for mot in freq_totale.keys()],
        }).sort_values(by="term_frequency", ascending=False)

        # Retourner toutes les informations sous forme de dictionnaire
        return {
            "vocabulaire": vocab,
            "freq_totale": freq_totale,
            "freq_documents": freq_documents,
            "freq_table": freq.head(n)  
        }

