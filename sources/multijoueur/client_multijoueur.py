from sys import exit  # for exit()
from sources.multijoueur.constantes_multijoueur import Carte
from sources.constantes_globales import *
from sources.multijoueur.liaison_serveur_client import EchangeServeurClient  # Custom network class


class Bouton:
    def __init__(self, valeur, couleur, x, y):
        """
        | Description : Créé un objet physique
        | Entrée : <str> (valeur de la carte) -- <str> (couleur de la carte) -- <int> (position x) -- <int> position y
        | Sortie : None
        """
        self.valeur = valeur
        self.couleur = couleur
        self.x, self.y = x, y

        # Si l'objet est la Pioche
        if valeur == "Pioche":
            self.hauteur = 192
            self.largeur = 128
            self.image = pygame.image.load("images/cartes/carte_cachee.png")
            self.image = pygame.transform.scale(self.image, (self.largeur, self.hauteur))

    def afficher(self, fenetre):
        """
        | Description : Affiche à l'écran l'objet (instance)
        | Entrée : <Surface> (fenêtre de jeu)
        | Sortie : None
        """
        fenetre.blit(self.image, (self.x, self.y))

    def est_cliquee(self, pos):
        """
        | Description : Renvoie si oui ou non l'objet (instance) est cliquée
        | Entrée : <tuple> (tuple de coordonnées de clic (x, y))
        | Sortie : <bool> (Objet cliqué ?)
        """
        clic_x, clic_y = pos[0], pos[1]
        if self.x <= clic_x <= self.x + self.largeur and self.y <= clic_y <= self.y + self.hauteur:
            return True
        else:
            return False


# Basically a button, just based on a card instead of on text and color
class CarteAffichee(Bouton):
    def __init__(self, carte: Carte, x, y, valeur, couleur):
        """
        | Description : Créé une carte de jeu à afficher
        | Entree : <class> (Carte) -- <int> (position x) -- <int> (position y) -- <str> (valeur de la carte) -- <str> (couleur de la carte)
        | Sortie : None
        """
        super().__init__(valeur, couleur, x, y)
        self.info_carte = carte
        self.couleur = carte.couleur
        self.largeur = 128
        self.hauteur = 192

        # La carte est-elle dans le paquet de l'adversaire ?
        if valeur == couleur == "retournee":
            # Oui : afficher une carte masquée
            self.image = pygame.image.load("images/cartes/carte_cachee.png")
            self.image = pygame.transform.scale(self.image, (self.largeur, self.hauteur))
        else:
            # Non : afficher la carte avec sa valeur et sa couleur
            self.image = pygame.image.load("images/cartes/" + couleur + "_" + valeur + ".png")
            self.image = pygame.transform.scale(self.image, (self.largeur, self.hauteur))
        self.valeur = str(carte.valeur)
        self.x, self.y = x, y

    def afficher(self, fenetre):
        """
        | Description : Affiche à l'écran la carte
        | Entrée : <Surface> (fenêtre de jeu)
        | Sortie : None
        """
        fenetre.blit(self.image, (self.x, self.y))


cartes_affichees = []  # Liste des cartes du joueur qui sont affichées à l'écran
pioche = Bouton("Pioche", None, 768, 444)  # Définit l'objet cliquable qui servira de pioche

arriere_plan = pygame.transform.scale(pygame.image.load("images/fond_jeu.png").convert_alpha(), (1920, 1080))  # Charge l'image d'arrière plan du jeu


def actualiser_fenetre(fenetre, variables_jeu, id_joueur):
    """
    | Description : Actualise la fenêtre du jeu
    | Entrée : <Surface> (fenêtre de jeu) -- <any> (collection des variables du jeu) -- <int> (ID du joueur dont c'est le tour)
    """

    global cartes_affichees

    fenetre.blit(arriere_plan, (0, 0))  # Affiche l'arrière plan dans la fenêtre de jeu

    # Si il n'y a pas deux joueurs de connectés, on affiche un texte d'attente
    if not (variables_jeu.connexion_reussie()):
        chargement_multi = pygame.transform.scale(pygame.image.load("images/chargement_multi.png").convert_alpha(), (1920, 1080))  # Charge l'image d'arrière plan du jeu
        fenetre.blit(chargement_multi, (0, 0))

    # Si il y a les deux joueurs de connectés
    else:

        # Affiche la dernière carte jouée
        derniere_carte = CarteAffichee(variables_jeu.derniere_carte_jouee, 1024, 444, variables_jeu.derniere_carte_jouee.valeur, variables_jeu.derniere_carte_jouee.couleur)
        derniere_carte.afficher(fenetre)

        # Affiche la pioche
        pioche.afficher(fenetre)

        # Si c'est au tour du joueur actuel
        if variables_jeu.id_joueur == id_joueur:
            texte_tour_jeu = police.render("À vous de jouer", 1, (0, 0, 0))
            x_position = largeur_fenetre // 2 - texte_tour_jeu.get_width() // 2
            fenetre.blit(texte_tour_jeu, (x_position, hauteur_fenetre-192-texte_tour_jeu.get_height()))  # Affiche le texte d'indiquant à qui est le tour
        else:
            texte_tour_jeu = police.render("Votre adversaire joue", 1, (0, 0, 0))
            x_position = largeur_fenetre // 2 - texte_tour_jeu.get_width() // 2
            fenetre.blit(texte_tour_jeu, (x_position, hauteur_fenetre-192-texte_tour_jeu.get_height()))  # Affiche le texte d'indiquant à qui est le tour

        cartes_actualisees = []  # Liste des cartes du joueurs affichées

        # On définit les paquets en fonction du joueur actuel
        if id_joueur == 0:
            cartes_joueur = variables_jeu.paquet0
            cartes_adversaire = variables_jeu.paquet1
        else:
            cartes_joueur = variables_jeu.paquet1
            cartes_adversaire = variables_jeu.paquet0

        # Calculs pour centrer l'affichage des paquets des joueurs
        longueur_paquet_joueur = len(cartes_joueur) * 128
        longueur_paquet_adversaire = len(cartes_adversaire) * 128
        x_position_joueur = largeur_fenetre / 2 - longueur_paquet_joueur / 2
        y_position_joueur = hauteur_fenetre - 192
        x_position_adversaire = largeur_fenetre / 2 - longueur_paquet_adversaire / 2
        y_position_adversaire = 0

        # Pour chaque carte du paquet du joueur, on affiche à l'écran la carte
        for carte in cartes_joueur:
            carte_a_afficher = CarteAffichee(carte, x_position_joueur, y_position_joueur, carte.valeur, carte.couleur)  # Charge l'image de la carte correspondante
            x_position_joueur += 128  # Décale la position de la future carte pour faire un paquet visuellement
            carte_a_afficher.afficher(fenetre)  # Affiche la carte
            cartes_actualisees.append(carte_a_afficher)

        # Pour chaque carte du paquet de l'adversaire, on affiche à l'écran la carte
        for carte in cartes_adversaire:
            carte_a_afficher = CarteAffichee(carte, x_position_adversaire, y_position_adversaire, "retournee", "retournee")  # Carte masquée car paquet de l'adversaire
            x_position_adversaire += 128  # Décale la position de la future carte pour faire un paquet visuellement
            carte_a_afficher.afficher(fenetre)  # Affiche la carte

        cartes_affichees = cartes_actualisees  # Met à jour les cartes déjà affichées

        if not cartes_adversaire or not cartes_joueur:
            from sources.multijoueur.ecran_victoire import ecran_fin
            ecran_fin()
            return False

    pygame.display.update()  # Actualise la fenêtre de jeu
    return True


def action_est_valide(future_carte: Carte, variables_jeu) -> bool:
    """
    | Description : Vérifie si la carte sélectionnée par le joueur peut être jouée (même couleur ou même valeur que la dernière carte jouée)
    | Entrée : <class> (La carte à tester) -- <any> (les derniers attributs de la partie enregistrés)
    | Sortie : <bool> (Carte autorisée ?)
    """
    derniere_carte_jouee = variables_jeu.derniere_carte_jouee
    # On vérifie si la couleur ou la valeur de la future est identique à la dernière carte en jeu
    if (future_carte.valeur == derniere_carte_jouee.valeur) or (future_carte.couleur == derniere_carte_jouee.couleur) or (future_carte.couleur == "noir"):
        return True
    return False


def multijoueur(addresse_saisie):
    running = True
    global cartes_affichees

    clock = pygame.time.Clock()  # Initialise le rafraichissement de l'écran
    try:
        echange_reseau = EchangeServeurClient(addresse_saisie)  # Classe qui échange les requêtes Serveur - Client
        id_joueur_actuel = echange_reseau.id_joueur_actuel()  # Récupère l'ID du joueur qui doit jouer (0, 1)
        pygame.time.delay(50)  # On attend afin que la connexion Serveur - Client se créé

        while running:  # Tant que l'on joue
            try:
                variables_jeu = echange_reseau.send("obtenir")  # Récupère la collection de variable du jeu en cours (dernière carte jouée, paquets de carte des joueurs, à qui le tour est...)
            except Exception as erreur:
                print("Connexion perdue", erreur)
                break

            for event in pygame.event.get():  # Récupère les évènements (clic de souris, frappe de clavier...)
                # Si le jeu est quitté
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Si on clique avec la souris
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Si c'est au client de jouer
                    if variables_jeu.id_joueur == id_joueur_actuel:
                        pos = pygame.mouse.get_pos()  # Récupère les coordonnées du clic de la souris

                        if 609 <= pos[0] <= 908 and 796 <= pos[1] <= 894 and not variables_jeu.connexion_reussie():
                            running = False
                            echange_reseau.client.close()
                            return False, None

                        # Si la pioche est cliquée et que le jeu est démarré
                        if pioche.est_cliquee(pos) and variables_jeu.connexion_reussie():
                            # On met à jour la partie en envoyant la requête 'piocher' au serveur -> Le joueur pioche une carte
                            variables_jeu = echange_reseau.send("piocher")

                        for carte in cartes_affichees:  # Pour chaque carte du paquet du joueur

                            # Si la carte est cliquée et que le jeu est démarré
                            if carte.est_cliquee(pos) and variables_jeu.connexion_reussie():

                                # Si la carte peut être jouée
                                if action_est_valide(carte.info_carte, variables_jeu):
                                    try:
                                        echange_reseau.send("jouer")  # On envoie la requête pour jouer une carte
                                        echange_reseau.send(carte.info_carte)  # On envoie la carte à jouer au serveur

                                    except EOFError as erreur:
                                        print("EOF recd.", erreur)
                                        pass

            clock.tick(10)  # Rafraîchit la fenêtre 10 fois par seconde
            running = actualiser_fenetre(fenetre, variables_jeu, id_joueur_actuel)  # Met à jour la fenêtre de jeu
        return False, None
    except Exception as erreur:
        return "mauvaise ip", erreur
