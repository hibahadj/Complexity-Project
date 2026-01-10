"""menu.py - Menu à choix multiples
M1 BIOINFO - ALGO Av. et Complexité

Interface console pour manipuler un arbre n-aire (degré 4) stocké en représentation chainée
(premier fils / frère suivant).
"""

from node import ArbreNaire
from operations import (
	creer_racine,
	ajouter_fils,
	afficher_profondeur,
	afficher_largeur,
	calculer_hauteur,
	rechercher,
	chemin_entre_noeuds,
	inserer_noeud,
	modifier_noeud,
	supprimer_noeud,
	afficher_sous_arbre,
	est_arbre_complet,
	sous_arbre_complet_maximal,
	extraire_sous_arbre,
	transformer_en_arbre_binaire,
	afficher_binaire_preordre,
	evaluation_experimentale,
	construire_arbre_vecteur_exemple1,
	construire_arbre_vecteur_exemple2,
	afficher_arbre_vecteur,
	afficher_graphique_tkinter,
)


def const_arbre1():
	"""Construit l'arbre exemple (comme dans l'ancien main.py)."""
	arbre = ArbreNaire(degre=4)
	racine = creer_racine(arbre, "A")

	b = ajouter_fils(arbre, racine, "B")
	c = ajouter_fils(arbre, racine, "C")
	d = ajouter_fils(arbre, racine, "D")
	e = ajouter_fils(arbre, racine, "E")

	f = ajouter_fils(arbre, b, "F")
	g = ajouter_fils(arbre, b, "G")

	ajouter_fils(arbre, c, "H")

	ajouter_fils(arbre, d, "I")
	ajouter_fils(arbre, d, "J")

	ajouter_fils(arbre, e, "K")

	ajouter_fils(arbre, f, "L")
	ajouter_fils(arbre, f, "M")
	ajouter_fils(arbre, g, "N")

	return arbre


def const_arbre2():
	"""Construit un 2e exemple (non complet) pour tester les opérations."""
	arbre = ArbreNaire(degre=4)
	r = creer_racine(arbre, "R")

	a = ajouter_fils(arbre, r, "A")
	b = ajouter_fils(arbre, r, "B")
	c = ajouter_fils(arbre, r, "C")

	ajouter_fils(arbre, a, "A1")
	a2 = ajouter_fils(arbre, a, "A2")
	ajouter_fils(arbre, a2, "A21")

	ajouter_fils(arbre, b, "B1")
	# pas d'enfant pour C

	return arbre


def _print_menu():
	print("\n" + "=" * 60)
	print("MENU - ARBRES N-AIRES (degré 4)")
	print("=" * 60)
	print("1) Construire exemple 1")
	print("2) Construire exemple 2")
	print("3) Afficher DFS")
	print("4) Afficher BFS")
	print("5) Hauteur")
	print("6) Rechercher un nœud")
	print("7) Chemin entre 2 nœuds")
	print("8) Insérer un nœud")
	print("9) Modifier un nœud")
	print("10) Supprimer un nœud")
	print("11) Afficher un sous-arbre")
	print("12) Vérifier si l'arbre est complet")
	print("13) Sous-arbre complet maximal")
	print("14) Extraire un sous-arbre (copie)")
	print("15) Transformer en arbre binaire (préordre)")
	print("16) Évaluation expérimentale (tableau)")
	print("17) Affichage graphique (tkinter)")
	print("18) Exemples représentation vecteur")
	print("0) Quitter")


def _need_tree(arbre):
	if arbre is None or arbre.racine is None:
		print(" Arbre vide. Choisissez d'abord 1 ou 2 pour construire un arbre.")
		return False
	return True


def lancer_menu():
	arbre = None

	while True:
		_print_menu()
		choix = input("\nVotre choix: ").strip()

		if choix == "0":
			print("Au revoir.")
			return

		if choix == "1":
			arbre = const_arbre1()
			print(" Arbre exemple 1 construit.")
			afficher_largeur(arbre)
			continue

		if choix == "2":
			arbre = const_arbre2()
			print(" Arbre exemple 2 construit.")
			afficher_largeur(arbre)
			continue

		if choix == "3":
			if not _need_tree(arbre):
				continue
			afficher_profondeur(arbre.racine)
			continue

		if choix == "4":
			if not _need_tree(arbre):
				continue
			afficher_largeur(arbre)
			continue

		if choix == "5":
			if not _need_tree(arbre):
				continue
			print(f"Hauteur: {calculer_hauteur(arbre)}")
			continue

		if choix == "6":
			if not _need_tree(arbre):
				continue
			info = input("Info à rechercher: ").strip()
			n = rechercher(arbre, info)
			if n:
				parent = n.parent.info if n.parent else "RACINE"
				print(f" Trouvé: {n.info} (parent={parent}, enfants={n.nb_enfants()})")
			else:
				print(" Non trouvé.")
			continue

		if choix == "7":
			if not _need_tree(arbre):
				continue
			a_info = input("Info du nœud a: ").strip()
			b_info = input("Info du nœud b: ").strip()
			a = rechercher(arbre, a_info)
			b = rechercher(arbre, b_info)
			chemin = chemin_entre_noeuds(a, b)
			if not chemin:
				print(" Chemin introuvable.")
			else:
				print("Chemin: " + " → ".join(n.info for n in chemin))
			continue

		if choix == "8":
			if not _need_tree(arbre):
				continue
			p = input("Info du parent: ").strip()
			x = input("Info du nouveau nœud: ").strip()
			inserer_noeud(arbre, p, x)
			afficher_largeur(arbre)
			continue

		if choix == "9":
			if not _need_tree(arbre):
				continue
			old = input("Info à modifier: ").strip()
			new = input("Nouvelle info: ").strip()
			modifier_noeud(arbre, old, new)
			afficher_largeur(arbre)
			continue

		if choix == "10":
			if not _need_tree(arbre):
				continue
			info = input("Info du nœud à supprimer: ").strip()
			supprimer_noeud(arbre, info)
			afficher_largeur(arbre)
			continue

		if choix == "11":
			if not _need_tree(arbre):
				continue
			info = input("Info racine du sous-arbre: ").strip()
			n = rechercher(arbre, info)
			if n is None:
				print(" Nœud non trouvé.")
			else:
				afficher_sous_arbre(n)
			continue

		if choix == "12":
			if not _need_tree(arbre):
				continue
			print("Complet" if est_arbre_complet(arbre) else "Non complet")
			continue

		if choix == "13":
			if not _need_tree(arbre):
				continue
			racine, taille = sous_arbre_complet_maximal(arbre)
			if racine is None:
				print(" Aucun sous-arbre complet.")
			else:
				print(f"Sous-arbre complet maximal: racine={racine.info}, taille={taille}")
				afficher_sous_arbre(racine)
			continue

		if choix == "14":
			if not _need_tree(arbre):
				continue
			info = input("Info racine du sous-arbre à extraire: ").strip()
			sous = extraire_sous_arbre(arbre, info)
			if sous is None:
				continue
			print("Sous-arbre extrait (copie) - BFS:")
			afficher_largeur(sous)
			continue

		if choix == "15":
			if not _need_tree(arbre):
				continue
			racine_b = transformer_en_arbre_binaire(arbre)
			print("Préordre binaire:")
			afficher_binaire_preordre(racine_b)
			continue

		if choix == "16":
			tailles = [10, 20, 30, 40, 50, 100]
			res = evaluation_experimentale(tailles, degre=4)
			print("\nTableau expérimental (secondes):")
			print(f"{'n':>6} | {'Tps complet':>12} | {'Tps sous-arbre complet max':>24}")
			print("-" * 50)
			for n, t1, t2 in res:
				print(f"{n:>6} | {t1:>12.6f} | {t2:>24.6f}")
			continue

		if choix == "17":
			if not _need_tree(arbre):
				continue
			afficher_graphique_tkinter(arbre)
			continue

		if choix == "18":
			print("\n1) Exemple vecteur 1")
			print("2) Exemple vecteur 2")
			sub = input("Votre choix: ").strip()
			if sub == "1":
				av = construire_arbre_vecteur_exemple1(degre=4)
				afficher_arbre_vecteur(av)
			elif sub == "2":
				av = construire_arbre_vecteur_exemple2(degre=4)
				afficher_arbre_vecteur(av)
			else:
				print(" Choix invalide.")
			continue

		print(" Choix invalide.")

