import socket  # Interaction Serveur-Client
import os  # Infos sur l'Interface
from _thread import *
from sources.multijoueur.systeme_de_jeu import Game  # Charge le système de jeu
from multiprocessing.connection import Listener  # Module pour gérer les connexions multiples et actions simulatnées des clients sur le serveur
from sources.multijoueur.constantes_multijoueur import tableaux_serveur  # Fonction qui permet l'affichage des tableaux dans les scripts


adresse_ip = socket.gethostbyname(socket.gethostname())  # Adresse IP du Serveur
port = 32769  # Port d'écoute
s = Listener((adresse_ip, port))  # Récupère les connexions entrantes

nombre_joueurs_connectes = 0  # Nombre de joueurs connectés au serveur


# Ensemble pour stocker les connexions actives
connexions = set()


# Dictionnaire pour stocker les tours de jeu, avec l'ID du tour comme clé
# Ce dictionnaire enregistre les tours de jeu au fur et à mesure du déroulement, ainsi, dès que c'est au tour d'un joueur, une nouvelle entrée dans le dictionnaire et créée
dico_tours_de_jeu = dict()

# ID du joueur actuel (0, 1)
# Etant donné qu'il n'y a que deux joueurs, une entrée du dictionnaire sur deux concerne le joueur actuel, celles qui sont de même parité (pair ou impair)
compteur_id_joueur = 0


def affiche(nombre_joueurs_connectes):
	"""
	| Description : Affiche un tableau avec des informations user-friendly pour jouer au jeu
	| Entrée : <int> (nombre de joueurs connectés)
	| Sortie : None
	"""
	tableau_serveur = tableaux_serveur(adresse_ip)  # Récupère la liste des tableaux possibles
	type_os = os.name  # Récupère le type de système d'exploitation
	if type_os == "nt":  # Si l'interface est un ordinateur sous Windows
		os.system('cls')  # Efface la console
	else:  # Sinon systèmes d'exploitation sous UNIX
		os.system('clear')  # Efface la console
	print(tableau_serveur[nombre_joueurs_connectes])  # Affiche le tableau correspondant au nombre de joueurs connectés


affiche(0)  # Affiche le tableau de statut du serveur


# Fonction exécutée dans un thread pour gérer la communication avec un client
def interaction_client(client, id_joueur, id_partie_actuelle, dico_tours_de_jeu):
	"""
	| Description : s'occupe du renvoi des données du jeu aux clients connectés au serveur
	| Entrée : <Connection> (la connexion avec le client) -- <int> (le joueur actuel, dont c'est le tour) -- <int> (le tour de jeu catuel) -- <dict> (l'historique des tours de jeu)
	| Sortie : None
	"""
	global compteur_id_joueur
	client.send(id_joueur)
	global nombre_joueurs_connectes
	nombre_joueurs_connectes += 1
	if nombre_joueurs_connectes > 2:
		nombre_joueurs_connectes -= 2
	affiche(nombre_joueurs_connectes)

	while True:  # Boucle infinie du serveur

		try:
			# Réception des données du client
			donnes_recues = client.recv()

			if id_partie_actuelle in dico_tours_de_jeu:
				# On récupère la partie du jeu en cours
				partie_en_cours = dico_tours_de_jeu[id_partie_actuelle]

				if not donnes_recues:
					print("Aucune donnée reçue")
					break

				else:
					
					# Client demande infos sur le statut du jeu
					if donnes_recues == "obtenir":
						reponse = partie_en_cours
						client.send(reponse)

					# Lorsqu'une carte est jouée
					if donnes_recues == "jouer":
						action_jouee = client.recv()
						deplacement_carte = action_jouee
						partie_en_cours.play(id_joueur, deplacement_carte)

						dico_tours_de_jeu[id_tour_jeu_catuel] = partie_en_cours
						reponse = partie_en_cours
						client.send(reponse)

					# Lorsque l'on pioche
					if donnes_recues == "piocher":
						partie_en_cours.piocher(id_joueur)

						dico_tours_de_jeu[id_tour_jeu_catuel] = partie_en_cours
						reponse = partie_en_cours
						client.send(reponse)

					# Fin du tour du joueur
					if donnes_recues == "fin_de_tour":
						partie_en_cours.finir_tour()
						dico_tours_de_jeu[id_tour_jeu_catuel] = partie_en_cours

						client.send(partie_en_cours)

			else:
				# print("Tous les joueurs sont déconnectés")
				nombre_joueurs_connectes = 0
				affiche(nombre_joueurs_connectes)
				break

		except Exception as erreur:
			# print(erreur)
			nombre_joueurs_connectes -= 1
			affiche(nombre_joueurs_connectes)
			break

	try:
		del dico_tours_de_jeu[id_tour_jeu_catuel]
	except Exception as erreur:
		# print(erreur)
		pass
	compteur_id_joueur -= 1
	client.close()


while True:
	# Attente de connexion d'un client
	client = s.accept()
	# Incrémentation du compteur d'ID
	compteur_id_joueur += 1

	id_joueur = 0  # Initialisation du numéro de joueur (0 par défaut)

	# On récupère le joueur à qui c'est le tour, en réalité, le reste de la division euclidienne nous permet d'obtenir la parité pour déterminer quel joueur doit jouer
	id_tour_jeu_catuel = (compteur_id_joueur - 1)//2

	if compteur_id_joueur % 2 == 1:
		dico_tours_de_jeu[id_tour_jeu_catuel] = Game(id_tour_jeu_catuel)
	else:
		dico_tours_de_jeu[id_tour_jeu_catuel].ready = True
		id_joueur = 1

	# On démarre une interaction avec les clients (joueurs) connectés au serveur
	start_new_thread(interaction_client, (client, id_joueur, id_tour_jeu_catuel, dico_tours_de_jeu))
