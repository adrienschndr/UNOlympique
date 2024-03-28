import importlib.util


def verification(bibliotheque):
    """
    | Description : Vérifie si une bibliothèque est installée dans Python ou non
    | Entrée : <str> (nom d'une bibliothèque)
    | Sortie : <bool> (La bibliothèque existe ?)
    """
    test_bibliotheque = importlib.util.find_spec(bibliotheque)
    if test_bibliotheque is not None:  # Si la bibliothèque existe
        return True
    else:  # Si elle n'existe pas
        return False


# Liste des bibliothèques à vérifier
liste_bibliotheques_utilisees = ['socket', 'os', '_thread', 'multiprocessing', 'sys', 'pygame', 'traceback', 'random', 'importlib.util']
compteur_erreurs = 0

print("Vérification des bibliothèques installées :")

for bibliotheque in liste_bibliotheques_utilisees:
    if verification(bibliotheque):
        print(f"| ✅ | {bibliotheque}")
    else:
        print(f"| ❌ | {bibliotheque}")
        compteur_erreurs += 1
if compteur_erreurs == 0:
    print("\n=> Toutes les bibliothèques requises sont installées. Vous pouvez lancer le jeu.")
