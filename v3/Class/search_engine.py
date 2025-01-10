import numpy as np
from collections import defaultdict
from scipy.sparse import csr_matrix

class SearchEngine:
    def __init__(self, source):
        """
        Initialise le moteur de recherche avec un objet de type Source.
        La matrice Documents x Termes est construite automatiquement.

        :param source: Objet contenant les sources et les documents (type source).
        """
        self.source = source
        self.vocab = {}
        self.mat_TF = None
        self.documents = []  

        # Construire la matrice Documents x Termes
        self._build_vocab_and_matrix()

    # Utilisation de Chat GPT afin de comprendre comment contruire la matrice Documents x Termes
    def _build_vocab_and_matrix(self):
        """
        Construit le vocabulaire et la matrice Documents x Termes (TF).
        """
        rows, cols, data = [], [], []
        vocab_index = {} 
        current_doc_id = 0
        
        # Parcourir les sources pour construire le vocabulaire et la matrice
        for _, source_obj in self.source.items():
            # Appel à stats pour récupérer le vocabulaire et les fréquences
            stats_result = source_obj.stats()
            vocab_source = stats_result["vocabulaire"]

            # Mettre à jour le vocabulaire global avec les mots de la source
            for mot, infos in vocab_source.items():
                if mot not in self.vocab:
                    self.vocab[mot] = {
                        "id": len(self.vocab), 
                        "occurrences": infos["occurrences"],
                        "document_frequency": infos["document_frequency"],
                    }
                    vocab_index[mot] = self.vocab[mot]["id"]
                else:
                    # Mettre à jour les fréquences globales
                    self.vocab[mot]["occurrences"] += infos["occurrences"]
                    self.vocab[mot]["document_frequency"] += infos["document_frequency"]

            # Construire la matrice TF pour les documents de la source
            for _, doc in source_obj.production.items():
                texte_nettoye = source_obj.nettoyer_texte(doc.full_content)
                mots = texte_nettoye.split()
                freq_doc = defaultdict(int)

                # Compter les occurrences dans le document
                for mot in mots:
                    if mot in vocab_index:
                        freq_doc[mot] += 1

                # Ajouter les données à la matrice TF
                for mot, count in freq_doc.items():
                    rows.append(current_doc_id)
                    cols.append(vocab_index[mot])
                    data.append(count)

                # Stocker le document dans la liste globale
                self.documents.append(doc)
                current_doc_id += 1

        # Construire la matrice sparse
        self.mat_TF = csr_matrix((data, (rows, cols)), shape=(len(self.documents), len(self.vocab)))

    def get_vocab(self):
        """
        Retourne le vocabulaire construit par le moteur de recherche.

        :return: Dictionnaire vocabulaire contenant les mots et leurs informations.
        """
        return self.vocab

    def get_matrix(self):
        """
        Retourne la matrice Term Frequency (TF).

        :return: Matrice sparse csr_matrix.
        """
        return self.mat_TF

    def search(self, query, nb_doc):
        """
        Recherche les documents les plus pertinents pour une requête donnée.

        :param query: Mots-clés de la requête (str).
        :param nb_doc: Nombre de documents à retourner (int).
        :return: Liste des documents les plus pertinents avec leurs scores.
        """
        # Nettoyer et vectoriser la requête
        query = query.lower()
        mots = query.split()
        query_vector = np.zeros(len(self.vocab))
        for mot in mots:
            if mot in self.vocab:
                query_vector[self.vocab[mot]["id"]] = 1  

        # Calculer les similarités avec les documents
        doc_vectors = self.mat_TF.toarray() 
        query_norm = np.linalg.norm(query_vector)
        doc_norms = np.linalg.norm(doc_vectors, axis=1)
        similarity = np.dot(doc_vectors, query_vector) / (doc_norms * query_norm + 1e-10)

        # Trier les scores et récupérer les documents les plus pertinents
        non_zero_indices = np.where(similarity > 0)[0]
        top_indices = np.argsort(similarity)[::-1][:nb_doc]
        results = [(self.documents[idx], similarity[idx]) for idx in top_indices if similarity[idx] > 0]

        return results, len(non_zero_indices)
    
    
    def get_word_stats(self, word):
        """
        Récupère les statistiques d'un mot dans le vocabulaire.

        :param word: Le mot pour lequel on veut obtenir les statistiques (str).
        :return: Un dictionnaire contenant les statistiques du mot, ou None si le mot n'existe pas.
        """
        word = word.lower()  
        if word in self.vocab:
            stats = self.vocab[word]
            return {
                "occurrences": stats["occurrences"],
                "document_frequency": stats["document_frequency"],
                "length": len(word)
            }
        else:
            return None


    