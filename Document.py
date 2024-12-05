class Document:
    # Constructeur de la classe Document
    def __init__(self, source_nom, auteur, titre, description, url, urlImage, datePubication, contenu):
        """
        Initialise une instance de la classe Document avec les informations fournies.
        
        :param source_nom: Nom de la source 
        :param auteur: Auteur du document
        :param titre: Titre du document
        :param description: Brève description du contenu
        :param url: Lien URL du document
        :param urlImage: URL de l'image associée
        :param datePubication: Date de publication
        :param contenu: Contenu complet du document
        """
        self.source_nom = source_nom
        self.auteur = auteur
        self.titre = titre
        self.description = description
        self.url = url
        self.urlImage = urlImage
        self.datePubication = datePubication
        self.contenu = contenu

    # Getters
    def get_source_nom(self):
        """Retourne le nom de la source."""
        return self.source_nom

    def get_auteur(self):
        """Retourne le nom de l'auteur."""
        return self.auteur

    def get_titre(self):
        """Retourne le titre du document."""
        return self.titre

    def get_description(self):
        """Retourne la description du document."""
        return self.description

    def get_url(self):
        """Retourne l'URL du document."""
        return self.url

    def get_urlImage(self):
        """Retourne l'URL de l'image associée."""
        return self.urlImage

    def get_datePubication(self):
        """Retourne la date de publication du document."""
        return self.datePubication

    def get_contenu(self):
        """Retourne le contenu complet du document."""
        return self.contenu

    # Setters
    def set_source_nom(self, source_nom):
        """Modifie le nom de la source."""
        self.source_nom = source_nom

    def set_auteur(self, auteur):
        """Modifie le nom de l'auteur."""
        self.auteur = auteur

    def set_titre(self, titre):
        """Modifie le titre du document."""
        self.titre = titre

    def set_description(self, description):
        """Modifie la description du document."""
        self.description = description

    def set_url(self, url):
        """Modifie l'URL du document."""
        self.url = url

    def set_urlImage(self, urlImage):
        """Modifie l'URL de l'image associée."""
        self.urlImage = urlImage

    def set_datePubication(self, datePubication):
        """Modifie la date de publication du document."""
        self.datePubication = datePubication

    def set_contenu(self, contenu):
        """Modifie le contenu complet du document."""
        self.contenu = contenu

    # Méthode spéciale pour afficher une représentation sous forme de chaîne
    def __str__(self):
        """
        Retourne une représentation en chaîne de l'objet Document.
        :return: Chaîne décrivant le document
        """
        return f"Document : {self.titre} de {self.auteur}"
