from math import sqrt, pi
import matplotlib.pyplot as plt 
from generation_aleatoire import genere_entier, genere_decimal, transforme

def est_dans_cercle(x, y):
    return sqrt(x * x + y * y) <= 1

def tirage(etat_actuel, n_max):
    etat, x = genere_decimal(etat_actuel, n_max)
    etat, y = genere_decimal(etat, n_max)
    resultat = est_dans_cercle(x, y)
    return etat, resultat

def compte_points_dans_cercle(etat, nb_tirages, n_max):
    nb_points_dans_cercle = 0
    for _ in range(nb_tirages):
        etat, point_dans_cercle = tirage(etat, n_max)
        if point_dans_cercle:
            nb_points_dans_cercle += 1
    return nb_points_dans_cercle

def estime_pi(etat_initial, nb_points, n_max):
    nb_points_dans_cercle = compte_points_dans_cercle(etat_initial, nb_points, n_max)
    proportion = nb_points_dans_cercle / nb_points
    pi_estimé = 4 * proportion
    return pi_estimé

def calculer_erreur_relative(valeur_estimée, valeur_reelle):
    erreur_relative = abs(valeur_estimée - valeur_reelle) / valeur_reelle * 100
    return erreur_relative

# Programme principal
if __name__ == "__main__":
    etat_initial = 55  # État initial pour la génération pseudo-aléatoire
    nb_points = 10000  # Nombre de points tirés
    n_max = 1000       # Bornes pour les nombres décimaux (au millième près)
    data = []

    etat = etat_initial
    for _ in range(nb_points):
        etat = genere_entier(etat)
        nombre = transforme(etat, n_max) * n_max 
        data.append(int(nombre))  

    # Afficher un histogramme
    plt.hist(data, bins=50, edgecolor="black")
    plt.title("Histogramme des nombres générés entre 0 et 1000")
    plt.xlabel("Valeurs")
    plt.ylabel("Fréquence")
    plt.show()

    # Estimation de pi
    pi_approx = estime_pi(etat_initial, nb_points, n_max)
    print(f"Estimation de π avec {nb_points} points : {pi_approx}")

    # Calcul de l'erreur relative
    erreur_relative = calculer_erreur_relative(pi_approx, pi)
    print(f"Erreur relative de l'estimation : {erreur_relative:.2f}%")
