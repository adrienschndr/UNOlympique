from constantes_globales import *


def menu_choix_ip():
    ecran_accueil = pygame.transform.scale(pygame.image.load("images/choix_ip_serveur.png").convert_alpha(),
                                           (1920, 1080))  # Charge l'image d'arrière plan du jeu
    running = True
    clock = pygame.time.Clock()  # Initialise le rafraichissement de l'écran
    addresse_saisie = ""
    while running:
        fenetre.blit(ecran_accueil, (0, 0))
        clock.tick(10)
        texte_ip = police.render(addresse_saisie, 1, (0, 0, 0))
        x_position = 750 - texte_ip.get_width() // 2
        fenetre.blit(texte_ip,
                     (x_position, 704 - (texte_ip.get_height() // 2)))  # Affiche le texte d'indiquant à qui est le tour
        pygame.display.flip()
        for event in pygame.event.get():  # Récupère les évènements (clic de souris, frappe de clavier...)
            # Si le jeu est quitté
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Appuyer sur Entrée pour arrêter
                    running = False
                    from multijoueur.client_multijoueur import multijoueur
                    bonne_ip = multijoueur(addresse_saisie)[0]
                    if bonne_ip == "mauvaise ip":
                        running = True
                        addresse_saisie = ""
                elif event.key == pygame.K_BACKSPACE:  # Retour arrière
                    addresse_saisie = addresse_saisie[:-1]
                else:
                    addresse_saisie += event.unicode
            # Si on clique avec la souris
            if event.type == pygame.MOUSEBUTTONDOWN:
                clic_x, clic_y = pygame.mouse.get_pos()
                if 609 <= clic_x <= 908 and 796 <= clic_y <= 894:
                    running = False
                    menu_principal()
                    break
                if 950 <= clic_x <= 1050 and 656 <= clic_y <= 756:
                    running = False
                    from multijoueur.client_multijoueur import multijoueur
                    bonne_ip = multijoueur(addresse_saisie)[0]
                    if bonne_ip == "mauvaise ip":
                        running = True
                        addresse_saisie = ""


def menu_principal():
    ecran_accueil = pygame.transform.scale(pygame.image.load("images/ecran_accueil.png").convert_alpha(), (1920, 1080))  # Charge l'image d'arrière plan du jeu
    running = True
    clock = pygame.time.Clock()  # Initialise le rafraichissement de l'écran
    while running:
        fenetre.blit(ecran_accueil, (0, 0))
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
                if 609 <= clic_x <= 908 and 512 <= clic_y <= 615:
                    running = False
                    from monojoueur.jeu_solo import monojoueur
                    monojoueur()
                if 609 <= clic_x <= 908 and 655 <= clic_y <= 756:
                    running = False
                    menu_choix_ip()
                if 609 <= clic_x <= 908 and 796 <= clic_y <= 894:
                    running = False
                    pygame.quit()
