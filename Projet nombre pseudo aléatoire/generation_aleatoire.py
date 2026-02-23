def genere_entier(etat_actuel):
    etat1 = (etat_actuel ^ (etat_actuel<<13)) % 2**32
    etat2 = (etat1 ^ (etat1>>17)) % 2**32
    etat_suivant = (etat2 ^ (etat2<<5)) % 2**32
    return etat_suivant

def transforme(etat_actuel, n_max):
    nombre_borné = etat_actuel % n_max
    nombre_décimal = nombre_borné/n_max
    return nombre_décimal

def genere_decimal(etat_actuel, n_max):
    etat_suivant = genere_entier(etat_actuel)
    valeur_transormée = transforme(etat_suivant, n_max)
    return etat_suivant, valeur_transormée

if __name__ == "__main__":
    print("bonjour")
    etat = 55 #etat initial
    etat = genere_entier(etat)
    print(etat)
    etat = genere_entier(etat)
    print(etat)
    etat = genere_entier(etat)
    print(etat)
    assert(transforme(447,568))
    etat, Valeur = genere_decimal(etat, 1000)
else:
    print("no")
print(__name__)
print("bjr")
etat_test=0
#while etat_test < 15:
 #   print(genere_decimal(etat_test, 10))
 #   etat_test = etat_test + 1