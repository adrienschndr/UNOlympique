from constantes_globales import *


def ecran_victoire(gagnant):
    if gagnant == "joueur":
        fond_fin_de_partie = pygame.transform.scale(pygame.image.load("images/ecran_victoire.png").convert_alpha(), (1920, 1080))
    else:
        fond_fin_de_partie = pygame.transform.scale(pygame.image.load("images/ecran_defaite.png").convert_alpha(), (1920, 1080))

    running = True
    clock = pygame.time.Clock()  # Initialise le rafraichissement de l'écran
    while running:
        fenetre.blit(fond_fin_de_partie, (0, 0))
        clock.tick(10)
        pygame.display.update()

        for event in pygame.event.get():  # Récupère les évènements (clic de souris, frappe de clavier...)
            # Si le jeu est quitté
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Si on clique avec la souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                clic_x, clic_y = pygame.mouse.get_pos()
                if 513 <= clic_x <= 808 and 839 <= clic_y <= 942:
                    running = False
                    from sources.menu import menu_principal
                    menu_principal()
                if 1111 <= clic_x <= 1411 and 843 <= clic_y <= 943:
                    running = False
                    pygame.quit()
