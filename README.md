<p align="center">
  <a href="https://github.com/sebanc/brunch" title="Brunch">
   <img src="https://i.imgur.com/Uu54bjE.png"alt="Logo"/>
  </a>
</p>

UNOlympique est une adaptation du jeu _Uno_ en Python, jeu vidéo bien connu du grnad public.
Le jeu propose deux modes de jeu :
- « SOLO » : joueur contre ordinateur
- « DUO » : joueur contre joueur, [voir instructions de mise en place](https://github.com/adrienschndr/UNOlympique?tab=readme-ov-file#-configurer-le-mode--duo-)

***
# 📦 Dépendences

UNOlympique utilise la bibliothèque `Pygame`.
Il est important d'avoir la dernière version de la bibliothèque pour que le jeu s'execute correctement, exécutez dans un Terminal (cmd) :
```sh
pip install -I 'pygame>=2.5.2' 
```
Aussi, le jeu utilise les bibliothèques suivantes, pré-installées avec Python : 

`socket`, `os`, `_thread`, `multiprocessing`, `sys`, `traceback`, `random`, `importlib.util`

Pour vous assurer que toutes les bibliothèques sont configurées proprement, vous pouvez lancer le *script* `verifier_bibliotheques.py`.
***

# 🕹️ Comment jouer ?
- [Télécharger le jeu](https://codeload.github.com/adrienschndr/UNOlympique/zip/refs/heads/main) puis extraire les fichiers du jeu
- Ouvrir le dossier `UNOlympique-main`
- Lancer le _script_ `demarrer_jeu.py`
***

# 🆚 Configurer le mode « DUO »
## ℹ️ Description
UNOlympique vous permet de jouer à deux joueurs simultanément, sur deux ordinateurs.

Pour se faire, vous devez au préalable avoir deux ordinateurs :
- Qui possèdent toutes les dépendences nécessaires au lancement du jeu.
- Qui sont connectés au même réseau.
- Dont au moins un des deux ordinateurs soit basé sur Windows et possède les droits d'administrateur.

## 📑 Instructions
### 1️⃣ Sur l'ordinateur qui possède les droits d'administrateur
- [Télécharger le jeu](https://codeload.github.com/adrienschndr/UNOlympique/zip/refs/heads/main) puis extraire les fichiers du jeu
- Ouvrir le dossier `UNOlympique-main`
- Lancez le *script* `demarrer_serveur.py`
> **Note** : Il est possible que votre ordinateur affiche une fenêtre concernant le pare-feu Windows. 
<details>
  <summary>👉 Cliquez ici si vous avez une fenêtre « Pare-feu Windows » 👈</summary>
  
[![N|Solid](https://i.imgur.com/mixm19G.png)]( )

> Cette fenêtre vous demande si vous souhaitez autoriser Python à laisser d'autres ordinateurs se connecter à celui-ci.
Cela est nécessaire afin que les joueurs puissent se connecter à un même serveur pour pouvoir s'affronter.

- **Pensez à cocher les DEUX cases (Réseaux privés ET Réseaux publics)**
</details>

- Dans la console, devrait s'afficher un tableau semblable à celui-ci :


```
-----------------------------------------------------------------
| 🚪 | Adresse IP du serveur            | 127.0.1.1             |
| ✅ | Statut du serveur                | Connecté              |
| ⏳ | En attente de joueurs...         | 0 / 2                 |
-----------------------------------------------------------------
```
> Note : Vous pouvez obtenir une adresse IP différente que celle mise dans l'exemple (`127.0.1.1`).
Une adresse IP est l'adresse où se trouve votre ordinateur au sein d'un réseau informatique. Elle devra être renseignée par les joueurs qui veulent s'affronter.

- Retenez l'adresse IP affichée sur VOTRE tableau.
- Tout en laissant le _script_ `demarrer_serveur.py` fonctionner en arrière_plan, lancez le _script_ `demarrer_jeu.py`.
- Une fois le jeu lancé, cliquez sur « DUO », puis, tapez l'IP inscrite sur le tableau. Puis appuyez sur `<Entrée>` ou cliquez sur le bouton de validation.<br />
✅ Si le jeu affiche « En attente d'un adversaire... », Félicitations ! Votre serveur est opérationnel est vous êtes prêt à jouer !<br />
❌ Si l'IP que vous venez d'écrire disparaît, vous avez fait une erreur dans le processus. Relisez attentivement le guide.

### 2️⃣ Sur l'autre ordinateur
- [Télécharger le jeu](https://codeload.github.com/adrienschndr/UNOlympique/zip/refs/heads/main) puis extraire les fichiers du jeu
- Ouvrir le dossier `UNOlympique-main`
- Lancer le _script_ `demarrer_jeu.py`
- Une fois le jeu lancé, cliquez sur « DUO », puis, tapez l'IP inscrite sur le tableau. Puis appuyez sur `<Entrée>` ou cliquez sur le bouton de validation

Les deux ordinateurs sont alors dans la même partie de UNO et les joueurs peuvent alors s'affronter.
***
# ⚖️ Mentions légales
Le jeu UNO est une marque déposée appartenant à Mattel, Inc. La société détient les droits sur le jeu et la propriété intellectuelle qui y est associée, y compris la conception des cartes et les règles du jeu. 

Les logos des Jeux Olympiques et des Jeux Paralympiques sont déposés respectivement par le Comité International Olympique (CIO) et le Comité International Paralympique (CIP) et en détiennent les droits exclusifs.

La mascotte des Jeux Olympiques de Paris 2024 ainsi que le logo officiel des Jeux Olympiques de Paris 2024 sont la propriété du Comité d'organisation des Jeux Olympiques et Paralympiques de Paris 2024 (COJO Paris 2024) et en détiennent les droits exclusifs.
