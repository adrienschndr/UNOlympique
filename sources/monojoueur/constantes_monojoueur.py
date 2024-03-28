# Importation des bibliothèques
import pygame

from routines_piles import *

clock = pygame.time.Clock()


# Définie les caractéristiques des cartes
class Carte(pygame.sprite.Sprite):
    def __init__(self, valeur, couleur):
        super().__init__()
        self.valeur = valeur
        self.couleur = couleur
        self.texture = pygame.image.load("images/cartes/" + couleur + "_" + valeur + ".png")
        self.texture = pygame.transform.scale(self.texture, (128, 192))
        self.image = pygame.Surface((self.texture.get_width(), self.texture.get_height()))
        self.rect = self.image.get_rect()
        self.rect.center = (self.rect.width/2, self.rect.height/2)
        self.image.blit(self.texture, (self.rect.x, self.rect.y))


class PaquetCartes:
    def __init__(self, nom_joueur, hauteur_graphique=None, liste_carte=None, pioche=None):
        if liste_carte is None:
            liste_carte = []
        self.nom_joueur = nom_joueur
        self.liste_carte = liste_carte
        if hauteur_graphique is not None:
            self.hauteur_graphique = hauteur_graphique
        if pioche is not None:
            for carte in range(7):
                nouvelle_carte = depiler(pioche.liste_carte)
                self.liste_carte.append(nouvelle_carte)
            self.pygamegroup = pygame.sprite.Group(self.liste_carte)

    def jouer_carte(self, id_carte, pile_de_jeu, ordre_de_jeu):
        carte_jouee = self.liste_carte.pop(id_carte)  # Retire la carte du paquet
        empiler(carte_jouee, pile_de_jeu)  # Ajoute la carte à la pile de jeu
        self.pygamegroup = pygame.sprite.Group(self.liste_carte)
        valeurs_cartes_fin_de_tour = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "plus2"]
        if carte_jouee.valeur in valeurs_cartes_fin_de_tour:
            ordre_de_jeu[0], ordre_de_jeu[1] = ordre_de_jeu[1], ordre_de_jeu[0]

    def update(self, events, pile_de_jeu, pioche, ordre_de_jeu):
        adversaire = ordre_de_jeu[1]
        derniere_carte = sommet(pile_de_jeu)
        if self.nom_joueur == "joueur":
            for id_carte in range(len(self.liste_carte)):
                carte = self.liste_carte[id_carte]
                for event in events:
                    if event.type == pygame.MOUSEBUTTONUP:
                        if carte.rect.collidepoint(event.pos):
                            # On vérifie si la carte peut être jouée ou non (valeurs ou couleurs identiques)
                            if carte.valeur == derniere_carte.valeur or carte.couleur == derniere_carte.couleur:
                                if carte.valeur == "plus2":
                                    piocher(2, pioche, adversaire)
                                self.jouer_carte(id_carte, pile_de_jeu, ordre_de_jeu)
                                return
        if self.nom_joueur == "ordinateur":
            for id_carte in range(len(self.liste_carte)):
                carte = self.liste_carte[id_carte]
                if carte.couleur == derniere_carte.couleur or carte.valeur == derniere_carte.valeur:
                    if carte.valeur == "plus2":
                        piocher(2, pioche, adversaire)
                    self.jouer_carte(id_carte, pile_de_jeu, ordre_de_jeu)
                    return
            piocher(1, pioche, self)
            ordre_de_jeu[0], ordre_de_jeu[1] = ordre_de_jeu[1], ordre_de_jeu[0]
            return

    def affiche(self):
        print("")
        texte = "Votre paquet de cartes : \t"
        for i in range(len(self.liste_carte)):
            texte += "   " + self.liste_carte[i].valeur + " - " + self.liste_carte[i].couleur + "   |"
        print(texte[:-1])
        print(" ")


# Sert à piocher une carte
def piocher(nombre_de_cartes, pioche, joueur):
    if taille(pioche) < nombre_de_cartes:
        nombre_de_cartes = taille(pioche)
    for repetition in range(nombre_de_cartes):
        joueur.liste_carte.append(depiler(pioche))
    joueur.pygamegroup = pygame.sprite.Group(joueur.liste_carte)
