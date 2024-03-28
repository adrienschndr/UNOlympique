# Importations des modules nécessaires
import traceback
import random
from sources.multijoueur.constantes_multijoueur import Carte, liste_toutes_cartes


def affiche(liste_carte):
    """
    | Description : Affiche dans la console le contenu du paquet mis en paramètre de la fonction
    | Entrée : <list>
    | Sortie : None
    """
    print("")
    texte = "Votre paquet de cartes : \t"
    for i in range(len(liste_carte)):
        texte += "   " + liste_carte[i].valeur + " - " + liste_carte[i].couleur + "   |"
    print(texte[:-1])
    print(" ")


class Game:
    def __init__(self, id_jeu):
        self.id_joueur = 0  # À quel joueur est-ce le tour ? (0 ou 1)
        self.ready = False  # Les deux joueurs sont-ils connectés ? (True ou False)
        self.id = id_jeu
        self.pioche = liste_toutes_cartes  # Charge la pioche
        random.shuffle(self.pioche)  # Mélange la pioche
        self.paquet0 = self.pioche[0:7]  # Définit le paquet du joueur 1 avec les 7 premières cartes de la pioche
        self.paquet1 = self.pioche[7:14]  # Définit le paquet du joueur 2 avec les 7 cartes suivantes de la pioche
        self.derniere_carte_jouee = self.pioche[14]  # Première carte jouée
        self.nb_cartes_utilisees = 15  # À partir de quelle carte la pioche peut être utilisée ?
        self.wins = [0, 0]

    def get_last_move(self):
        """
        | Description : Récupère la dernière carte jouée
        | Entrée : None
        | Sortie : <class>
        """
        return self.derniere_carte_jouee

    def finir_tour(self):
        """
        | Description : Lorsque le joueur a fini de jouer, on change self.id_joueur en 0 ou en 1, pour passer au joueur suivant
        | Entrée : None
        | Sortie : None
        """
        self.id_joueur = (self.id_joueur + 1) % 2

    def play(self, id_joueur, carte_jouee: Carte):
        """
        | Description : Gère les actions produites lorsqu'une carte est jouée
        | Entrée : <int> (Quel joueur : 0/1) -- <class> (Carte jouée)
        | Sortie : None
        """

        # Si carte jouée est spéciale (+2, passe, inverse)
        if carte_jouee.valeur == "plus2":  # Si carte jouée est un +2
            if id_joueur == 0:  # On ajoute à l'adversaire deux cartes dans sont paquet
                self.paquet1.append(self.pioche[self.nb_cartes_utilisees])
                self.paquet1.append(self.pioche[self.nb_cartes_utilisees + 1])
            else:  # On ajoute à l'adversaire deux cartes dans sont paquet
                self.paquet0.append(self.pioche[self.nb_cartes_utilisees])
                self.paquet0.append(self.pioche[self.nb_cartes_utilisees + 1])
            self.nb_cartes_utilisees += 2  # On incrémente de 2 le nombre de carte déjà utilisées
        if carte_jouee.valeur == "passe" or carte_jouee.valeur == "inverse":
            pass
        # Sinon on joue normalement
        else:
            # On passe au joueur suivant
            self.id_joueur = (id_joueur + 1) % 2

        # On retire du paquet du joueur la carte qu'il a jouée
        try:
            # Cette condition permet de savoir à quel joueur on doit retirer la carte de son paquet (joueur0 ou joueur1)
            if id_joueur == 0:
                index = self.find_card(carte_jouee, id_joueur)  # On vérifie que la carte est bien dans le paquet
                if index is not None:
                    self.paquet0.pop(index)  # On retire la carte du paquet du joueur
            else:
                index = self.find_card(carte_jouee, id_joueur)  # On vérifie que la carte est bien dans le paquet
                if index is not None:
                    self.paquet1.pop(index)  # On retire la carte du paquet du joueur
            self.derniere_carte_jouee = carte_jouee  # On met à jour la dernière carte jouée
        except Exception as e:
            print(traceback.format_exc(), e)

    def connexion_reussie(self):
        """
        | Description : Renvoie le statut du jeu, si les deux joueurs sont connectés ou non
        | Entrée : None
        | Sortie : <bool>
        """
        return self.ready

    def find_card(self, carte_a_tester: Carte, id_joueur):
        """
        | Description : Cherche dans un paquet de carte une carte en particulier
        | Entrée : <class> (Carte à vérifier) -- <int> (ID du joueur)
        | Sortie : <int> || None
        """

        # On sélectionne le paquet du bon joueur
        if id_joueur == 0:
            paquet_joueur = self.paquet0
        else:
            paquet_joueur = self.paquet1

        for index in range(0, len(paquet_joueur)):  # On parcourt le paquet du joueur
            if paquet_joueur[index] == carte_a_tester:  # Comparaison rendue possible avec constructeur __eq__ (Classe Carte)
                return index  # Renvoie la position de la carte dans le paquet du joueur

        return None  # Si carte non trouvée

    def piocher(self, id_joueur):
        """
        | Description : Fait piocher une carte à un joueur
        | Entrée : <int> (ID du joueur)
        | Sortie : None
        """
        if id_joueur == 0:
            self.paquet0.append(self.pioche[self.nb_cartes_utilisees])  # On ajoute la carte suivante de la pioche
        else:
            self.paquet1.append(self.pioche[self.nb_cartes_utilisees])  # On ajoute la carte suivante de la pioche
        self.nb_cartes_utilisees += 1  # On incrémente de 1 le nombre de carte déjà utilisées
        self.finir_tour()
