from Class.Document import Document

class DocumentFactory:
    @staticmethod
    def create_document(data):
        """
        Crée un objet Document à partir d'un dictionnaire de données.

        :param data: Dictionnaire contenant les informations nécessaires pour créer un Document.
        :return: Une instance de Document.
        """
        return Document(
            source_nom=data.get('source', {}).get('name', "Source inconnue") 
            if isinstance(data.get('source'), dict) else "Source inconnue",
            auteur=data.get('author', "Auteur inconnu"),
            titre=data.get('title', "Titre inconnu"),
            description=data.get('description', "Description indisponible"),
            url=data.get('url', None),
            urlImage=data.get('urlToImage', None),
            datePubication=data.get('publishedAt', None),
            contenu=data.get('content', "Contenu indisponible"),
            full_content=data.get('full_content', "Contenu complet indisponible")
        )