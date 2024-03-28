# Importation des bibliothèques
from random import *

import pygame.time

from sources.constantes_globales import *
from sources.monojoueur.constantes_monojoueur import *


# Création de la pioche
def creer_pioche():
    pile_de_jeu = creer_pile_vide()
    pioche = creer_pile_vide()
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

    shuffle(pioche)  # Mélange la pioche
    prochaine_carte = sommet(pioche)
    # Si carte spéciale mise en jeu au début de la partie
    while prochaine_carte.valeur == "plus2" or prochaine_carte.valeur == "passe" or prochaine_carte.valeur == "inverse":
        shuffle(pioche)  # Mélange la pioche
        prochaine_carte = sommet(pioche)
    empiler(depiler(pioche), pile_de_jeu)
    pioche = PaquetCartes("Pioche", None, pioche, None)
    return pioche, pile_de_jeu


def afficher_pioche(pioche):
    future_carte = sommet(pioche)
    future_carte.rect.x, future_carte.rect.y = 1024, 444
    image_carte = pygame.transform.scale(pygame.image.load("images/cartes/carte_cachee.png").convert_alpha(), (128, 192))
    fenetre.blit(image_carte, (future_carte.rect.x, future_carte.rect.y))
    return


def afficher_paquet(paquet):
    if paquet.nom_joueur == "ordinateur":
        longueur_paquet = len(paquet.liste_carte) * 128
        x = largeur_fenetre / 2 - longueur_paquet / 2
        texture_carte = pygame.transform.scale(pygame.image.load("images/cartes/carte_cachee.png"), (128, 192))
        for id_carte in range(len(paquet.liste_carte)):
            fenetre.blit(texture_carte, (x, 0))
            x += 128
    if paquet.nom_joueur == "joueur":
        longueur_paquet = len(paquet.liste_carte) * 128
        x = largeur_fenetre / 2 - longueur_paquet / 2
        for id_carte in range(len(paquet.liste_carte)):
            carte = paquet.liste_carte[id_carte]
            carte.rect.width = 128
            carte.rect.height = carte.rect.width * 1.5
            carte.rect.x, carte.rect.y = x, paquet.hauteur_graphique
            x += 128


def monojoueur():
    pioche, pile_de_jeu = creer_pioche()
    joueur = PaquetCartes("joueur", hauteur_fenetre - 192, None, pioche)
    ordinateur = PaquetCartes("ordinateur", 0, None, pioche)

    ordre_de_jeu = [joueur, ordinateur]
    background_png = pygame.transform.scale(pygame.image.load("images/fond_jeu.png").convert_alpha(), (1920, 1080))
    running = True
    dessus = ""
    while running:
        joueur_actuel = ordre_de_jeu[0]
        evenements = pygame.event.get()
        fenetre.blit(background_png, (0, 0))
        derniere_carte = sommet(pile_de_jeu)
        fenetre.blit(derniere_carte.texture, (768, 444))
        if est_vide(pioche.liste_carte):
            print("Vide")
            while not est_vide(pile_de_jeu):
                print(taille(pioche.liste_carte), taille(pile_de_jeu))
                if dessus == "":
                    dessus = depiler(pile_de_jeu)
                empiler(depiler(pile_de_jeu), pioche.liste_carte)
            shuffle(pioche.liste_carte)
            empiler(dessus, pile_de_jeu)
        afficher_pioche(pioche.liste_carte)
        if taille(pioche.liste_carte) == 0:
            image_carte = pygame.transform.scale(pygame.image.load("images/cartes/carte_cachee.png").convert_alpha(), (128, 192))
            fenetre.blit(image_carte, (1024, 444))
        clock.tick(60)
        joueur.pygamegroup.draw(fenetre)
        afficher_paquet(joueur)
        afficher_paquet(ordinateur)
        pygame.display.update()
        if joueur_actuel == joueur:
            joueur.update(evenements, pile_de_jeu, pioche.liste_carte, ordre_de_jeu)
        if joueur_actuel == ordinateur:
            ordinateur.update(evenements, pile_de_jeu, pioche.liste_carte, ordre_de_jeu)
        for event in evenements:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if sommet(pioche.liste_carte).rect.collidepoint(event.pos):
                    if joueur_actuel == joueur:
                        piocher(1, pioche.liste_carte, joueur)
                        ordre_de_jeu[0], ordre_de_jeu[1] = ordre_de_jeu[1], ordre_de_jeu[0]
        if not joueur.liste_carte:
            running = False
            from sources.monojoueur.ecran_victoire import ecran_victoire
            ecran_victoire(joueur.nom_joueur)
        if not ordinateur.liste_carte:
            running = False
            from sources.monojoueur.ecran_victoire import ecran_victoire
            ecran_victoire(ordinateur.nom_joueur)
