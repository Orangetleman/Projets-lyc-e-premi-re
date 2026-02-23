# Créé par dealmeida, le 25/02/2025 en Python 3.7

UN = "1"
DEUX = "2"
TROIS = "3"
QUATRE = "4"
CINQ = "5"
SIX = "6"
SEPT = "7"
HUIT = "8"
NEUF = "9"

def lire_fichier(chemin):
    with open(chemin)as f:
        contenu = f.readlines()
    return contenu

def créer_ligne(T_line):
    i=0
    e=0
    N_line = [None for i in range(9)]
    while e<11:
        if T_line[e]=="\n" or T_line[e]==" ":
            e+=1
        elif T_line[e]=="*":
            i+=1
            e+=1
        else:
            N_line[i] = int(T_line[e])
            i+=1
            e+=1
    return N_line

def créer_grille(chemin_grillle_incomplète):
    T_grille = lire_fichier(chemin_grillle_incomplète)
    N_grille = [[None for i in range(9)] for i in range(9)]
    i=0
    while i<9:
        N_grille[i] = créer_ligne(T_grille[i])
        i+=1
    return N_grille

"""def affiche_grille(grille):
    i = 0
    while i < len(grille):
        e = 0
        ligne = ""
        while e < 9:
            if grille[i][e] is None:
                ligne += "* "
            else:
                ligne += str(grille[i][e]) + " "
            e += 1
        print(ligne)
        i += 1"""

def affiche_grille(grille):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)  # Ligne horizontale après chaque bloc de 3 lignes

        ligne = ""
        for j in range(9):
            if j % 3 == 0 and j != 0:
                ligne += "| "  # Séparateur vertical entre les blocs de 3 colonnes

            ligne += str(grille[i][j]) if grille[i][j] is not None else "*"
            ligne += " "

        print(ligne)


if __name__ == "__main__":
    #print(lire_fichier("grille_incomplete.txt"))
    #print(créer_ligne(lire_fichier("ligne.txt")[0]))
    affiche_grille(créer_grille("grille_incomplete.txt"))
