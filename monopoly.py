from random import *

# Liste des occurences :
def initialiser_occurences():
    return []

# Carte du Plateau
def initialiser_plateau():
    return ['départ', 'boulevard bellevue', 'caisse de communeauté', 'rue lecourse',
            'impôts', 'gare montparnasse', 'rue de valigrand', 'chance', 'rue de courcelles', 
            'avenue de la république', 'simple visite', 'boulevard de la vilette', "compagnie d'électricité", 
            'avenue de neuilly', 'rue de paradis', 'gare de Lyon', 'avenue Mozart', 'caisse de communeauté', 
            'boulevard saint-michel', 'place pigaille', 'parc gratuit', 'avenue matignon', 'chance', 
            'boulevard malesherbes', 'avenue henri-martin', 'gare du nord', 'faubourg saint-honoré', 
            'place de la bourse', "compagnie de distribution d'eau", 'rue la fayette', 'en prison', 
            'avenue de breteuil', 'avenue de foch', 'caisse de communeauté', 'boulevard des capucins', 
            'gare saint-nazare', 'chance', 'avenue des champs-elysées', 'taxe de luxe', 'rue de la paix']

def initialiser_cartes_communeauté():
    return ['prison','case départ']

def initialiser_cartes_chance():
    return ['prison','case départ','boulevard de la vilette','avenue henri-martin','rue de la paix',
            'gare montparnasse','gare','gare','compagnie','recule']

####################

def nextcase(position, nombre, plateau):
    return plateau[(position + nombre) % len(plateau)]

def communeaute(position, plateau, cartes_communeauté, occurences):
    carte = None
    a = randint(0, 15)
    if a < 2:
        carte = cartes_communeauté[a]
    
    if carte is None: 
        return position, occurences

    if carte == 'prison':
        position, occurences = prison(position, occurences)
    else:
        position = 0
    
    return position, occurences

def chance(position, plateau, cartes_chance, occurences):
    carte = None
    a = randint(0, 15)
    if a < 10:
        carte = cartes_chance[a]
    
    if carte is None:
        return position, occurences

    if carte == 'prison':
        position, occurences = prison(position, occurences)
    elif carte == 'case départ':
        position = 0
        occurences.append('départ')
    elif carte == 'recule':
        position -= 3
        occurences.append(plateau[position])
    elif carte == 'gare':
        position, occurences = go_prochaine_gare(position, plateau, occurences)
    elif carte == 'compagnie':
        position, occurences = go_prochaine_compagnie(position, plateau, occurences)
    else:
        indexPlateau = get_postion(carte, plateau)
        occurences.append(carte)
        position = indexPlateau

    return position, occurences

def go_prochaine_gare(position, plateau, occurences):
    tempPosition = position
    currentCarte = plateau[position]

    while not currentCarte.startswith('gare'):
        tempPosition += 1
        currentCarte = plateau[tempPosition % len(plateau)]

    position = get_postion(currentCarte, plateau)
    occurences.append(currentCarte)
    return position, occurences

def go_prochaine_compagnie(position, plateau, occurences):
    tempPosition = position
    currentCarte = plateau[position]

    while not currentCarte.startswith('compagnie'):
        tempPosition += 1
        currentCarte = plateau[tempPosition % len(plateau)]

    position = get_postion(currentCarte, plateau)
    occurences.append(currentCarte)
    return position, occurences

def prison(position, occurences):
    occurences.append("en prison")
    return position, occurences

def tirer_de():
    return randint(1, 6)

def get_postion(case, plateau):
    for i in range(len(plateau)):
        if case == plateau[i]:
            return i

def calculer_nouvelle_case(des1, des2, position, plateau, occurences):
    case = nextcase(position, des1 + des2, plateau)
    position = get_postion(case, plateau)
    occurences.append(case)

    if case == 'caisse de communeauté':
        position, occurences = communeaute(position, plateau, initialiser_cartes_communeauté(), occurences)
    elif case == 'chance':
        position, occurences = chance(position, plateau, initialiser_cartes_chance(), occurences)
    elif case == 'en prison':
        position, occurences = prison(position, occurences)

    return position, occurences

def lancer_des(doubleNb, position, plateau, occurences):
    des1, des2 = tirer_de(), tirer_de()

    if doubleNb >= 3:
        position, occurences = prison(position, occurences)
        return False, position, occurences

    position, occurences = calculer_nouvelle_case(des1, des2, position, plateau, occurences)
    return des1 == des2, position, occurences

def tour(position, plateau, occurences):
    double = 0
    while True:
        doubleNb, position, occurences = lancer_des(double, position, plateau, occurences)
        if not doubleNb:
            break
        double += 1

def trie(liste):
    for i in range(len(liste)):
        echange = False
        for j in range(0, len(liste) - i - 1):
            if liste[j] > liste[j + 1]:
                liste[j], liste[j + 1] = liste[j + 1], liste[j]
                echange = True

        if not echange:
            break
    return liste


def get_last_index(x, old_list):
  for i in range(len(old_list)):
    if old_list[i] == x:
      return i

def afficher_statistique(occurences, nbTour, plateau):
    print("Statistiques des cases sur lequel on est tombé avec le pourcentage d'y tomber par tour")

    occurrences_nb = []
    for i in range(len(plateau)):
        occurrences_nb.append(0)

    for case in occurences:
        index = get_postion(case, plateau)
        occurrences_nb[index] += 1
    
    occurences_trie = trie(occurrences_nb)

    indices_affiches = []

    for x in occurences_trie:
        prev_index = get_last_index(x, occurrences_nb)
        
        if prev_index not in indices_affiches and occurrences_nb[prev_index] > 0:
            print(f"{plateau[prev_index]}: {occurrences_nb[prev_index]} fois ({round((occurrences_nb[prev_index] / nbTour) * 100, 2)}%)")
            indices_affiches.append(prev_index)



def main():
    print("Combien de tour voulez-vous simuler ?")
    nombre_tour = int(input())

    plateau = initialiser_plateau()
    occurences = initialiser_occurences()

    position = 0
    for i in range(nombre_tour):
        tour(position, plateau, occurences)

    afficher_statistique(occurences, nombre_tour, plateau)
 
main()
