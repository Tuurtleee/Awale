import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from collections import deque

# Chargement des fréquences des bigrammes depuis un fichier CSV
def charger_freq_bigrams(fichier):
    df = pd.read_csv(fichier, header=None)
    lettres = list('abcdefghijklmnopqrstuvwxyz')
    freq_bigrams = {}
    
    for i, lettre1 in enumerate(lettres):
        for j, lettre2 in enumerate(lettres):
            bigram = lettre1 + lettre2
            freq_bigrams[bigram] = df.iat[i, j]
    
    return freq_bigrams

# Fonction d'évaluation
def evaluer_configuration(config, freq_bigrams):
    score = 0
    for bigram, freq in freq_bigrams.items():
        pos1, pos2 = config.index(bigram[0]), config.index(bigram[1])
        distance = abs(pos1 - pos2)
        score += freq * distance
    return score

# Génération des voisins
def generer_voisins(config):
    voisins = []
    for i in range(len(config)):
        for j in range(i + 1, len(config)):
            voisin = config.copy()
            voisin[i], voisin[j] = voisin[j], voisin[i]
            voisins.append(voisin)
    return voisins

# Recherche tabou
def recherche_tabou(freq_bigrams, taille_liste_tabou, iterations):
    lettres = list('abcdefghijklmnopqrstuvwxyz')
    config_actuelle = np.random.permutation(lettres).tolist()
    meilleure_config = config_actuelle.copy()
    meilleure_valeur = evaluer_configuration(config_actuelle, freq_bigrams)
    
    liste_tabou = deque(maxlen=taille_liste_tabou)
    valeurs = [meilleure_valeur]

    for iteration in range(iterations):
        voisins = generer_voisins(config_actuelle)
        voisinage = [(voisin, evaluer_configuration(voisin, freq_bigrams)) for voisin in voisins]
        voisinage.sort(key=lambda x: x[1])
        
        for voisin, valeur in voisinage:
            if voisin not in liste_tabou:
                config_actuelle = voisin
                liste_tabou.append(voisin)
                if valeur < meilleure_valeur:
                    meilleure_config = voisin
                    meilleure_valeur = valeur
                break
        
        valeurs.append(meilleure_valeur)

        if iteration % 100 == 0:
            print(f"Iteration {iteration} - Meilleure valeur: {meilleure_valeur}")
    
    plt.plot(valeurs)
    plt.xlabel('Itérations')
    plt.ylabel('Valeur de la fonction objectif')
    plt.title('Évolution de la valeur de la fonction objectif')
    plt.show()

    return meilleure_config, meilleure_valeur

# Exemple d'utilisation
freq_bigrams = charger_freq_bigrams('map.csv')
meilleure_config, meilleure_valeur = recherche_tabou(freq_bigrams, taille_liste_tabou=50, iterations=1000)

# Affichage de la configuration finale
print("Meilleure configuration :")
for i in range(0, len(meilleure_config), 10):  # afficher 10 lettres par ligne
    print(" ".join(meilleure_config[i:i+10]))

print(f"Meilleure valeur de la fonction objectif: {meilleure_valeur}")
