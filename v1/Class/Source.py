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

