import os
import pygame


type_os = os.name
if type_os == "nt":  # Si l'interface est un ordinateur sous Windows
    os.system('cls')
else:
    os.system('clear')

pygame.init()

largeur_fenetre, hauteur_fenetre = 1920, 1080
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre), pygame.SCALED | pygame.FULLSCREEN)
pygame.display.set_caption("UNOlympique")
police = pygame.font.Font("police.ttf", 60)
