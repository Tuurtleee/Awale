import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Chargement des fréquences des bigrammes
def charger_freq_bigrams():
    freq_bigrams = {}
    #load map.csv
    df = pd.read_csv("map.csv", sep=' ', header=None)
    for i in range(len(df)):
        freq_bigrams[(df.iloc[i,0], df.iloc[i,1])] = df.iloc[i,2]
    return freq_bigrams

# Fonction d'évaluation
def evaluer_configuration(config, freq_bigrams):
    score = 0
    for bigram, freq in freq_bigrams.items():
        pos1, pos2 = config.index(bigram[0]), config.index(bigram[1])
        distance = abs(pos1 - pos2)
        score += freq * distance
    return score

# Recuit simulé
def recuit_simule(freq_bigrams, temp_initiale, taux_refroidissement, iterations, pas_rafraichissement):
    lettres = list('abcdefghijklmnopqrstuvwxyz')
    config_actuelle = np.random.permutation(lettres)
    meilleure_config = config_actuelle.copy()
    meilleure_valeur = evaluer_configuration(config_actuelle, freq_bigrams)
    
    temp = temp_initiale
    valeurs = [meilleure_valeur]

    for i in range(iterations):
        nouvelle_config = config_actuelle.copy()
        pos1, pos2 = np.random.randint(0, 26, size=2)
        nouvelle_config[pos1], nouvelle_config[pos2] = nouvelle_config[pos2], nouvelle_config[pos1]

        nouvelle_valeur = evaluer_configuration(nouvelle_config, freq_bigrams)
        delta = nouvelle_valeur - meilleure_valeur

        if delta < 0 or np.random.rand() < np.exp(-delta / temp):
            config_actuelle = nouvelle_config
            if nouvelle_valeur < meilleure_valeur:
                meilleure_config = nouvelle_config
                meilleure_valeur = nouvelle_valeur
        
        temp *= taux_refroidissement
        valeurs.append(meilleure_valeur)

        if i % pas_rafraichissement == 0:
            print(f"Iteration {i} - Meilleure valeur: {meilleure_valeur}")
    plt.plot(valeurs)
    plt.xlabel('Itérations')
    plt.ylabel('Valeur de la fonction objectif')
    plt.title('Évolution de la valeur de la fonction objectif')
    plt.show()

    return meilleure_config, meilleure_valeur

# Exemple d'utilisation
freq_bigrams = charger_freq_bigrams()
print(freq_bigrams)
meilleure_config, meilleure_valeur = recuit_simule(freq_bigrams, temp_initiale=1000, taux_refroidissement=0.99, iterations=10000, pas_rafraichissement=100)
print(f"Meilleure configuration: {meilleure_config}")
print(f"Meilleure valeur de la fonction objectif: {meilleure_valeur}")