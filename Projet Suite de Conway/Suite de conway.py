
def trouver_la_répétition(séquence):
    longueur = 1
    for i in range(1,len(séquence)):
        if séquence[i] == séquence[i-1]:
            longueur = longueur + 1
        elif séquence == "":
            longueur = "nul"
        else:
            break
    return(longueur,séquence[0])

def ajouter_chiffres(séquence2,chiffre1,chiffre2):
    nouvelle_séquence = séquence2 + str(chiffre_1) + str(chiffre_2)
    return(nouvelle_séquence)

def longueur_de_une_répétition(séquence3,indice_début_séquence):
    chiffre_concerné = séquence3[indice_début_séquence]
    longueur2 = 1
    for i in range(indice_début_séquence + 1,len(séquence3)):
        if séquence3[i] == chiffre_concerné:
            longueur2 = longueur2 + 1
        else:
            break
    return (longueur2,chiffre_concerné)

def prochain_terme_de_Conway(séquence):
    résultat = ""
    longueur = 1
    for i in range(1,len(séquence)):
        if séquence[i] == séquence[i-1]:
            longueur += 1
        else:
            résultat += str(longueur) + séquence[i-1]
            longueur = 1
    résultat += str(longueur) + séquence[-1]
    return résultat

def suite_de_Conway(N):
    if N < 0:
        N = N * (-1)
    elif N == 0:
        print("le nombre doit être positif")
    résultat = "1"
    for i in range(N):
        print(résultat)
        résultat = prochain_terme_de_Conway(résultat)
    return résultat

# Zone de demande à l'utilisateur :
séquence = input("Entrez une séquence de chiffres: ")

chiffre_1 = int(input("Entrez le premier chiffre à ajouter: "))
chiffre_2 = int(input("Entrez le second chiffre à ajouter: "))

indice_début_séquence = int(input("Indice du début de la séquence: "))



#Zone d'impression sur la console des résultats test
print(trouver_la_répétition(séquence))
print("nouvelle séquence :",ajouter_chiffres(séquence,chiffre_1,chiffre_2))
print(longueur_de_une_répétition(séquence,indice_début_séquence))
print(prochain_terme_de_Conway(séquence))
nombre_de_Conway = int(input("Entrez un nombre strictement positif: ")) #Question d'aesthetique
print(suite_de_Conway(nombre_de_Conway))