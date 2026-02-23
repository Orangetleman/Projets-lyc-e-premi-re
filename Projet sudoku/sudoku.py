# Créé par dealmeida, le 25/02/2025 en Python 3.7
from grille import créer_grille, affiche_grille
import random

def recherche_indice_élément(list,n):
    i=0
    while i<len(list):
        if list[i] == n:
            return i
        i+=1
    return None

def éléments_ligne(grille,N_line):
    return grille[N_line]

def éléments_colonne(grille,N_column):
    return [grille[i][N_column] for i in range(9)]

def éléments_carré(grille,N_column,N_line):
    C_list = []
    start_x, start_y = (N_column // 3) * 3, (N_line // 3) * 3
    for i in range(3):
        for j in range(3):
            C_list.append(grille[start_y + i][start_x + j])
    return C_list

def nombre_possible(grille,N_column,N_line):
    N_possibles=[i for i in range(1,10)]
    l_carré=éléments_carré(grille,N_column,N_line)
    l_ligne=éléments_ligne(grille,N_line)
    l_colone=éléments_colonne(grille,N_column)
    i_c=0
    for e_c in l_carré:
        indice = recherche_indice_élément(N_possibles, e_c)
        if indice is not None:
            N_possibles.pop(indice)

    for e_l in l_ligne:
        indice = recherche_indice_élément(N_possibles, e_l)
        if indice is not None:
            N_possibles.pop(indice)

    for e_co in l_colone:
        indice = recherche_indice_élément(N_possibles, e_co)
        if indice is not None:
            N_possibles.pop(indice)
    return N_possibles



def suivant(numero_ligne, numero_colonne):
    # la fonction retourne le prochain numéro de ligne et de colonne dans le parcourt
    if numero_colonne < 8:
        return numero_ligne , numero_colonne+1
    else:
        return numero_ligne+1 , 0

def retour_sur_trace(grille, numero_ligne, numero_colonne):
    # si le numero de ligne vaut 9 ou plus c'est qu'on a réussi à atteindre le bout de la grille en faisant des hypothèses
    # on a réussi a compléter toute la grille.
    if numero_ligne >= 9:
        return True

    numero_ligne_suivant, numero_colonne_suivant = suivant(numero_ligne, numero_colonne)

    # si la case actuelle n'est pas vide, alors on va tout de suite tester la case suivante.
    if grille[numero_ligne][numero_colonne] is not None:
        return retour_sur_trace(grille, numero_ligne_suivant, numero_colonne_suivant)

    # si on est ici, c'est que la case est vide, on cherche d'abord toutes les valeurs possibles pour cette case
    possibles = nombre_possible(grille, numero_colonne, numero_ligne)

    # on essaie toutes les valeurs
    for chiffre in possibles:
        # on essaie de placer ce chiffre dans grille
        # c'est une hypothèse
        grille[numero_ligne][numero_colonne] = chiffre

        # si nous avons réussi à remplir la fin de la grille à partir d'ici alors on a réussi.
        if retour_sur_trace(grille, numero_ligne_suivant, numero_colonne_suivant):
            return True

        # si on arrive ici c'est que notre hypothèse est fausse, on l'annule
        grille[numero_ligne][numero_colonne] = None

    # si on arrive ici c'est qu'aucune des valeurs testées ne fonctionne (ou qu'il n'y en a aucune)
    # nous avons fait une mauvaise hypothèse en amont, il est impossible de remplir la grille à partir d'ici.
    return False




if __name__ == "__main__":
    """Diréfents test de fonction:
    print(éléments_ligne(créer_grille("grille_incomplete.txt"),3))
    print(éléments_colonne(créer_grille("grille_incomplete.txt"),3))
    print(éléments_carré(créer_grille("grille_incomplete.txt"),2,1))
    print(recherche_indice_élément(éléments_carré(créer_grille("grille_incomplete.txt"),2,1),9))
    print(nombre_possible(créer_grille("grille_incomplete.txt"),2,1))"""
    grille = créer_grille("grille_incomplete.txt")
    if retour_sur_trace(grille, 0, 0):
        print("✅ Solution trouvée :")
    else:
        print("❌ Aucune solution possible.")

    affiche_grille(grille)


