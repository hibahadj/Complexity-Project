# Mini-projet Complexité — Arbres (n-aire, n=4)

Ce dépôt contient un mini-projet sur les **arbres n-aires (degré 4)**, leurs **représentations mémoire** (chaînée et vecteur) et des **opérations usuelles** avec un **menu console**.

## Fichier à exécuter (mono-fichier)
- Exécutable unique : [projet_complexite.py](projet_complexite.py)

## Prérequis
- Python 3.10+ (recommandé: 3.11)
- Aucun package externe
- (Optionnel) `tkinter` pour l’affichage graphique (option 17 du menu)

## Exécution (PC de l’enseignante)
Ouvrir un terminal dans le dossier et lancer :
- `python projet_complexite.py`

Sur certaines installations Windows :
- `py projet_complexite.py`

## Utilisation
Le programme affiche un menu. **Commencer par construire un arbre** :
- `1` : construit l’exemple 1
- `2` : construit l’exemple 2

Ensuite vous pouvez tester :
- DFS (profondeur), BFS (largeur)
- hauteur, recherche
- chemin entre 2 nœuds
- insertion / modification / suppression
- affichage d’un sous-arbre, extraction de sous-arbre
- vérification “arbre complet” et sous-arbre complet maximal
- transformation en arbre binaire (illustration)
- tableau d’évaluation expérimentale

### Format des entrées
Quand une option demande une information de nœud, il faut saisir **une seule étiquette** (ex: `A`, `B`, `C`, `A2`).
Une saisie du type `11,22,17` est considérée comme **une seule chaîne** et ne correspondra pas à un nœud.

## Rapport
- Rapport Markdown : [rapport.md](rapport.md)
- (Si présent) Rapport PDF : `rapport.pdf`

## Nettoyage (optionnel)
- [tempCodeRunnerFile.py](tempCodeRunnerFile.py) est un fichier temporaire VS Code et peut être supprimé.
