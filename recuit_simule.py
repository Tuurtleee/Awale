import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Fonction pour charger les fréquences des bigrammes depuis un fichier CSV
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
    
    score = 0  # Initialisation du score
    for bigram, freq in freq_bigrams.items():  # Pour chaque bigramme et sa fréquence
        if bigram[0] in config and bigram[1] in config:
            pos1 = config.index(bigram[0])  # Trouver la position de la première lettre du bigramme
            pos2 = config.index(bigram[1])  # Trouver la position de la deuxième lettre du bigramme
            x1, y1 = obtenir_position_2d(pos1, largeur)  # Convertir en coordonnées 2D
            x2, y2 = obtenir_position_2d(pos2, largeur)  # Convertir en coordonnées 2D
            distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)  # Calculer la distance euclidienne
            score += freq * distance  # Pondérer la distance par la fréquence et ajouter au score
    return score  # Retourner le score total

# Recuit simulé
def recuit_simule(freq_bigrams, temp_initiale, taux_refroidissement, iterations, pas_rafraichissement, largeur=10):
    lettres = list('abcdefghijklmnopqrstuvwxyz')
    configuration_initiale = lettres + [''] * (largeur * 4 - len(lettres))  # Ajout de cases vides
    config_actuelle = np.random.permutation(configuration_initiale).tolist()
    meilleure_config = config_actuelle.copy()
    meilleure_valeur = evaluer_configuration(config_actuelle, freq_bigrams, largeur)
    
    temp = temp_initiale
    valeurs = [meilleure_valeur]

    for i in range(iterations):
        nouvelle_config = config_actuelle.copy()
        # Sélectionner deux positions aléatoires pour l'échange
        pos1, pos2 = np.random.choice(len(nouvelle_config), 2, replace=False)
        nouvelle_config[pos1], nouvelle_config[pos2] = nouvelle_config[pos2], nouvelle_config[pos1]

        nouvelle_valeur = evaluer_configuration(nouvelle_config, freq_bigrams, largeur)
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
    
    plt.plot(valeurs, label='Recuit Simulé')

    # out in out.png
    #plt.savefig('last_recuit.png')

    return meilleure_config, meilleure_valeur

# Exemple d'utilisation
def run(iter, temp):
    freq_bigrams = charger_freq_bigrams('map.csv')
    meilleure_config, meilleure_valeur = recuit_simule(freq_bigrams, temp_initiale=temp, taux_refroidissement=0.99, iterations=iter, pas_rafraichissement=100)

    # Affichage de la configuration finale sans les cases vides
    print("Meilleure configuration :")
    for i in range(0, len(meilleure_config), 10):  # afficher 10 lettres par ligne
        print(" ".join(['_' if x == '' else x for x in meilleure_config[i:i+10]]))

    print(f"Meilleure valeur de la fonction objectif: {meilleure_valeur}")
    return meilleure_config, meilleure_valeur
