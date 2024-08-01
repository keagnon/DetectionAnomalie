""" Analysis"""
import pandas as pd
import matplotlib.pyplot as plt

# Données pour l'analyse financière en Euros
donnees_euros = {
    "Catégorie": [
        "Infrastructure",
        "Licences logicielles",
        "Administrateurs Systèmes",
        "Data Analyst",
        "Ingénieurs DevOps/Développeur Full Stack",
        "Ingénieurs ML",
        "Pertes de Productivité",
        "Opportunités Manquées"
    ],
    "Coûts directs (EUR)": [18000, 13500, 40000, 40000, 45000, 45000, 0, 0],
    "Coûts indirects (EUR)": [0, 0, 0, 0, 0, 0, 9000, 6300]
}

donnees_economies = {
    "Catégorie": [
        "Réduction des Coûts Énergétiques",
        "Optimisation des Opérations", "Éviter les Pannes Coûteuses"],
    "Économies estimées (EUR)": [22500, 13500, 16200]
}

# Création des DataFrames
df_euros = pd.DataFrame(donnees_euros)
df_economies = pd.DataFrame(donnees_economies)

fig, ax = plt.subplots(2, 1, figsize=(14, 14))

# Coûts directs et indirects
df_euros.plot(
    kind="bar", x="Catégorie",
    y=["Coûts directs (EUR)",
    "Coûts indirects (EUR)"],
    ax=ax[0], color=["orange", "red"])
ax[0].set_title("Analyse des Coûts Directs et Indirects")
ax[0].set_ylabel("Coût en EUR")
ax[0].set_xlabel("Catégories de Coûts")
ax[0].legend(["Coûts directs", "Coûts indirects"])

# Économies estimées
df_economies.plot(kind="bar", x="Catégorie",
y="Économies estimées (EUR)", ax=ax[1], color='green')
ax[1].set_title("Économies Potentielles Grâce à la Détection des Anomalies")
ax[1].set_ylabel("Économies en EUR")
ax[1].set_xlabel("Catégories de Coûts")
ax[1].legend(["Économies estimées"])

plt.tight_layout()
plt.savefig("analyse_financiere.png")
plt.show()


