# Importation des bibliothèques
import pygame
import os
import socket
from random import *
from routines_piles import *


def creer_fenetre():
    """
    | Description : Créé la fenêtre du jeu et initialise des constantes globales
    | Entrée : None
    | Sortie : <int> <int> <Surface> <str>
    """
    type_os = os.name
    if type_os == "nt":  # Si l'interface est un ordinateur sous Windows
        os.system('cls')
    else:
        os.system('clear')
    # adresse = input("Quelle IP serveur ? (votre IP est : " + str(socket.gethostbyname(
    #     socket.gethostname())) + ", appuyez sur <Entrée> si vous souhaitez être le joueur hôte) : ")
    adresse = "192.168.1.7"

    pygame.init()

    # Si adresse non précisée
    if adresse == "":
        adresse = socket.gethostbyname(socket.gethostname())  # Joueur local
    largeur_fenetre, hauteur_fenetre = 1920, 1080
    fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre), pygame.SCALED | pygame.FULLSCREEN)
    pygame.display.set_caption("UNOlympique")
    police = pygame.font.Font("../police.ttf", 60)
    return largeur_fenetre, hauteur_fenetre, fenetre, adresse, police


class Carte(pygame.sprite.Sprite):
    def __init__(self, valeur, couleur):
        """
        | Description : Définit une instance de <class> Carte
        | Entrée : <str> (valeur de la carte) -- <str> (couleur de la carte)
        | Sortie : None
        """
        super().__init__()
        self.valeur = valeur  # Valeur de la carte (0, 1, 2, ..., plus2, passe, inverse)
        self.couleur = couleur  # Couleur de la carte (rouge, bleu, jaune, vert)

    def __str__(self):
        """
        | Description : Affiche les propriétés d'une instance de <class>
        | Entrée : None
        | Sortie : <str>
        """
        return "----------\nCarte : \n - Valeur : " + self.valeur + "\n - Couleur : " + self.couleur + "\n----------"

    def __eq__(self, other):
        """
        | Description : Compare deux cartes
        | Entrée : <class> (autre carte à comparer)
        | Sortie : <bool> (sont-elles identiques ? => True/False)
        """
        if type(other) is str:
            return self.valeur == other and self.couleur == other
        return (self.valeur == other.valeur) and (self.couleur == other.couleur)


def creer_pioche():
    pioche = creer_pile_vide()  # Créé une pile vide
    liste_couleurs = ["rouge", "bleu", "vert", "jaune"]  # Différentes couleurs des cartes
    liste_valeurs = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "passe", "inverse",
                     "plus2"]  # Différentes valeurs des cartes
    for nb_repetition_carte in range(2):  # Répétition des cartes pour chaque couleur
        for couleur in liste_couleurs:
            for valeur in liste_valeurs:
                carte = Carte(valeur, couleur)  # Création des cartes
                empiler(carte, pioche)  # Ajoute les cartes dans la pioche
                if valeur == "0" and nb_repetition_carte == 1:  # Pour le zéro, cas spécial car il y en a qu'un par
                    # couleur
                    depiler(pioche)
    # for nb_repetition_carte in range(4):
    #     carte = Carte("joker", "noir")
    #     empiler(carte, pioche)  # Ajout des jokers dans la pioche
    #     carte = Carte("plus4", "noir")
    #     empiler(carte, pioche)  # Ajout des +4 dans la pioche

    shuffle(pioche)  # Mélange la pioche
    prochaine_carte = sommet(pioche)
    # Si carte spéciale mise en jeu au début de la partie
    while prochaine_carte.valeur == "plus2" or prochaine_carte.valeur == "passe" or prochaine_carte.valeur == "inverse":
        shuffle(pioche)  # Mélange la pioche
        prochaine_carte = sommet(pioche)
    return pioche


liste_toutes_cartes = creer_pioche()  # Créé la liste de toutes les cartes qui seront dans le jeu


def tableaux_serveur(adresse_ip):
    """
    | Description : Affiche un tableau avec des informations user-friendly pour jouer au jeu
    | Entrée : <str> (Adresse IP)
    | Sortie : <str> (Tableau ASCII)
    """
    tableaux_serveur = [
        f"""
-----------------------------------------------------------------
| ℹ️ | Adresse IP du serveur\t\t| {adresse_ip} \t\t|
| ✅ | Statut du serveur \t\t| Connecté \t\t|
| ⏳ | En attente de joueurs...\t\t| 0 / 2\t\t\t|
-----------------------------------------------------------------
    """,
        f"""
-----------------------------------------------------------------
| ℹ️ | Adresse IP du serveur\t\t| {adresse_ip} \t\t|
| ✅ | Statut du serveur \t\t| Connecté \t\t|
| ⏳ | En attente de joueurs...\t\t| 1 / 2\t\t\t|
-----------------------------------------------------------------
    """,
        f"""
-----------------------------------------------------------------
| ℹ️ | Adresse IP du serveur\t\t| {adresse_ip} \t\t|
| ✅ | Statut du serveur \t\t| Connecté \t\t|
| ✅ | Jeu en cours d'execution\t\t| 2 / 2\t\t\t|
-----------------------------------------------------------------
"""
    ]
    return tableaux_serveur
