import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

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
def evaluer_configuration(config, freq_bigrams, largeur=10):
    def obtenir_position_2d(index, largeur=10):
        """Convertit un index 1D en coordonnées 2D."""
        return divmod(index, largeur)
    
    score = 0
    for bigram, freq in freq_bigrams.items():
        if bigram[0] in config and bigram[1] in config:
            pos1 = config.index(bigram[0])
            pos2 = config.index(bigram[1])
            x1, y1 = obtenir_position_2d(pos1, largeur)
            x2, y2 = obtenir_position_2d(pos2, largeur)
            distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
            score += freq * distance
    return score

# Fonction de croisement
def croisement(parent1, parent2):
    taille = len(parent1)
    point = random.randint(1, taille - 1)
    enfant1 = parent1[:point] + [x for x in parent2 if x not in parent1[:point]]
    enfant2 = parent2[:point] + [x for x in parent1 if x not in parent2[:point]]
    return enfant1, enfant2

# Fonction de mutation
def mutation(config, prob_mutation):
    if random.random() < prob_mutation:
        pos1, pos2 = np.random.randint(0, len(config), size=2)
        config[pos1], config[pos2] = config[pos2], config[pos1]
    return config

# Algorithme génétique
def algorithme_genetique(freq_bigrams, taille_population, prob_mutation, generations, largeur=10):
    lettres = list('abcdefghijklmnopqrstuvwxyz')
    configuration_initiale = lettres + [''] * (largeur * 4 - len(lettres))  # Ajout de cases vides
    population = [np.random.permutation(configuration_initiale).tolist() for _ in range(taille_population)]
    meilleure_config = min(population, key=lambda x: evaluer_configuration(x, freq_bigrams, largeur))
    meilleure_valeur = evaluer_configuration(meilleure_config, freq_bigrams, largeur)
    
    valeurs = [meilleure_valeur]

    for generation in range(generations):
        population_eval = [(config, evaluer_configuration(config, freq_bigrams, largeur)) for config in population]
        population_eval.sort(key=lambda x: x[1])
        population = [config for config, score in population_eval[:taille_population // 2]]

        nouvelle_population = []
        while len(nouvelle_population) < taille_population:
            parents = random.sample(population, 2)
            enfant1, enfant2 = croisement(parents[0], parents[1])
            nouvelle_population.extend([mutation(enfant1, prob_mutation), mutation(enfant2, prob_mutation)])

        population = nouvelle_population
        meilleure_config_courante = min(population, key=lambda x: evaluer_configuration(x, freq_bigrams, largeur))
        meilleure_valeur_courante = evaluer_configuration(meilleure_config_courante, freq_bigrams, largeur)
        
        if meilleure_valeur_courante < meilleure_valeur:
            meilleure_config = meilleure_config_courante
            meilleure_valeur = meilleure_valeur_courante
        
        valeurs.append(meilleure_valeur)

        if generation % 100 == 0:
            print(f"Generation {generation} - Meilleure valeur: {meilleure_valeur}")
    #plt.clf()
    
    plt.plot(valeurs, label='Algorithme génétique')
    plt.xlabel('Générations')
    plt.ylabel('Valeur de la fonction objectif')
    plt.title('Évolution de la valeur de la fonction objectif')

    # save
    plt.savefig('last_genetique.png')
    plt.legend()

    return meilleure_config, meilleure_valeur

def run(taille_pop, iterations, mutprob):
    # Exemple d'utilisation
    freq_bigrams = charger_freq_bigrams('map.csv')
    meilleure_config, meilleure_valeur = algorithme_genetique(freq_bigrams, taille_pop, mutprob, iterations)

    # Affichage de la configuration finale
    print("Meilleure configuration :")
    for i in range(0, len(meilleure_config), 10):  # afficher 10 lettres par ligne
        print(" ".join(['_' if x == '' else x for x in meilleure_config[i:i+10]]))

    print(f"Meilleure valeur de la fonction objectif: {meilleure_valeur}")
    return meilleure_config, meilleure_valeur

# Exécution de la fonction
if __name__ == "__main__":
    run()
