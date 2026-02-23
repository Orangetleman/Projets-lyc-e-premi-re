import random
import matplotlib.pyplot as plt

def lance_dé():
    dé = random.randrange(1,7)
    return dé

def lance_plusieurs_dés(nombre_lancers):
    lancers = [0] * nombre_lancers
    for f in range(len(lancers)):
        lancers[f] = lance_dé()
    return lancers

def calcule_effectifs(population):
    effectif_valeurs = [0,0,0,0,0,0]
    i = 0
    for i in population :
        if i == 1 :
            effectif_valeurs[0] = effectif_valeurs[0] + 1
        if i == 2 :
            effectif_valeurs[1] = effectif_valeurs[1] + 1
        if i == 3 :
            effectif_valeurs[2] = effectif_valeurs[2] + 1
        if i == 4 :
            effectif_valeurs[3] = effectif_valeurs[3] + 1
        if i == 5 :
            effectif_valeurs[4] = effectif_valeurs[4] + 1
        if i == 6 :
            effectif_valeurs[5] = effectif_valeurs[5] + 1
    return effectif_valeurs

def calcule_somme(liste_entiers):
    somme = 0
    for j in liste_entiers:
        somme = somme + j
    return somme

def calcule_moyenne(liste_entiers):
    somme = 0
    moyenne = 0
    for h in liste_entiers:
        somme = somme + h
    moyenne = somme / len(liste_entiers)
    return moyenne

def calcule_erreur_absolue(effectifs):
    valeur_espérée = 0.0
    valeur_espérée = calcule_somme(effectifs) / 6
    erreur = [0.0,0.0,0.0,0.0,0.0,0.0]
    for g in range(len(effectifs)):
        erreur[g] = valeur_espérée - effectifs[g]
        if erreur[g] < 0 :
            erreur[g] = erreur[g] * -1.0
    return erreur

def calcule_erreur_relative(effectifs):
    erreur_rela = [0, 0, 0, 0, 0, 0]
    valeur_espérée = 0.0
    valeur_espérée = calcule_somme(effectifs) / 6
    erreur_abso = calcule_erreur_absolue(effectifs)
    for d in range(len(effectifs)):
        erreur_rela[d]= erreur_abso[d] / valeur_espérée * 100
    return erreur_rela


def affiche_diagramme_baton(effectifs, labels, titre):


    fig, ax = plt.subplots()

    numbers = ['1', '2', '3', '4','5','6']
    counts = effectifs
    bar_labels = ['red', 'blue', 'red', 'orange']
    bar_colors = ['red', 'orange', 'yellow', 'green','blue','purple']
    ax.bar(numbers, counts, label=bar_labels, color=bar_colors)

    ax.set_ylabel(labels)
    ax.set_title(titre)

    plt.show()


# Tests
assert len(lance_plusieurs_dés(100)) == 100

# Ajoute tes tests
assert (lance_dé() <= 6),(lance_dé() >= 1)
assert calcule_effectifs([5,1,2,2,6,3,4,4,4,5,3]) == [1,2,2,3,2,1]
assert calcule_somme([1,1564165831,5,4,8,6]) == 1564165855
assert calcule_moyenne([1,3,2,6,3,2,4,1,5,2,6,1]) == 3
assert calcule_erreur_absolue([3,2,5,3,4,7]) == [1, 2, 1, 1, 0, 3]
assert calcule_erreur_relative([3,2,5,3,4,7]) == [25, 50, 25, 25, 0, 75]
assert calcule_somme(calcule_erreur_relative([2,2,2,2,1,3])) == 100.0
print(calcule_somme(calcule_erreur_relative([int(input("rentrer le premier nombre")),int(input("rentrer le second nombre")),int(input("rentrer le troisième nombre")),int(input("rentrer le quatrième nombre")),int(input("rentrer le cinquième nombre")),int(input("rentrer le sixième nombre"))])))

# Programme principal
n = int(input()) # a changer plus tard ou demander a l'utilisateur
population = lance_plusieurs_dés(n)
effectifs = calcule_effectifs(population)
affiche_diagramme_baton(effectifs,"nombre d'apparition","apparission des chiffres par lancé")
print("Moyenne des lancers", calcule_moyenne(population))