import socket  # Module d'interaction Serveur-Client
from multiprocessing.connection import Client  # Module pour gérer les connexions multiples et actions simulatnées des clients sur le serveur
import traceback  # Module pour détailler les erreurs Serveurs - Clients


class EchangeServeurClient:
	def __init__(self, adresse_ip):
		"""
		| Description : Passerelle entre le client et le serveur, c'est cette classe qui gère les interactions entre interfaces, qui reçoit et envoie les données
		| Entrée : <str> (Adresse IP du serveur)
		| Sortie : None
		"""
		self.server = adresse_ip
		self.port = 32769
		self.client = Client((self.server, self.port))
		self.addr = (self.server, self.port)
		self.id_joueur = self.se_connecter()

	def id_joueur_actuel(self):
		return self.id_joueur

	def se_connecter(self):
		"""
		| Description : Etablit la connexion Serveur-Client si des données peuvent être échanges
		| Entrée : None
		| Sortie : None
		"""
		try:
			return self.client.recv()  # Essaye de recevoir les données du serveur
		except socket.error as erreur:  # Si c'est impossible de recevoir des données, alors il n'y a pas de connexion
			str(erreur)
			print("Impossible de se connecter", erreur)  # On affiche l'erreur

	def send(self, donnee):
		"""
		| Description : Echange des données entre le serveur et le client
		| Entrée : <any> (une donnée envoyée)
		| Sortie : <any> (une donnée échangée)
		"""

		# Le client peut soit envoyer une action (carte jouée), soit informer qu'il a tiré une carte.
		try:
			self.client.send(donnee)  # On envoie des données

			# Lorsqu'une carte est jouée, on n'attend pas de données retour donc on demande des données reçues que lorsque nécessaire
			if donnee != "jouer":
				donnee_recue = self.client.recv()
				return donnee_recue  # Données reçues du serveur

		except Exception as e:
			print(traceback.format_exc(), e)
