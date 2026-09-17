import matplotlib.pyplot as plt
import numpy as np

# ========================================================
# DATI
# ========================================================

categorie = [
    "Valutativi\npositivi",
    "Premi /\nriconoscimenti /\nsuccesso",
    "Novità /\nattesa",
    "Coinvolgimento\ndel lettore"
]

top25 = [
    0.170,
    0.329,
    0.470,
    0.129
]

resto = [
    0.281,
    0.129,
    0.302,
    0.019
]


# ========================================================
# POSIZIONI
# ========================================================

x = np.arange(len(categorie))

larghezza = 0.35


# ========================================================
# GRAFICO
# ========================================================

plt.figure(figsize=(11, 6))

barre_top25 = plt.bar(
    x - larghezza / 2,
    top25,
    larghezza,
    label="Top 25"
)

barre_resto = plt.bar(
    x + larghezza / 2,
    resto,
    larghezza,
    label="Posizioni 26–100"
)


# ========================================================
# VALORI SOPRA LE BARRE
# ========================================================

for barra in barre_top25:

    altezza = barra.get_height()

    plt.text(
        barra.get_x() + barra.get_width() / 2,
        altezza + 0.01,
        f"{altezza:.3f}",
        ha="center",
        va="bottom",
        fontsize=10
    )


for barra in barre_resto:

    altezza = barra.get_height()

    plt.text(
        barra.get_x() + barra.get_width() / 2,
        altezza + 0.01,
        f"{altezza:.3f}",
        ha="center",
        va="bottom",
        fontsize=10
    )


# ========================================================
# TITOLI
# ========================================================

plt.title(
    "Linguaggio promozionale: Top 25 vs posizioni 26–100",
    fontsize=14
)

plt.ylabel(
    "Occorrenze per 100 parole"
)

plt.xticks(
    x,
    categorie
)

plt.legend()


# ========================================================
# LAYOUT
# ========================================================

plt.tight_layout()

plt.show()
