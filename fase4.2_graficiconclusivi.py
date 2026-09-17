import matplotlib.pyplot as plt
import numpy as np


# ========================================================
# DATI
# ========================================================

termini = [
    "nuove",
    "attesissima",
    "nuovi",
    "nuova edizione",
    "appena uscito",
    "nuova",
    "fenomeno",
    "atteso",
    "nuovo romanzo",
    "nuovo"
]

differenze = [
    5,
    1,
    1,
    1,
    1,
    -2,
    -2,
    -2,
    -2,
    -12
]


# ========================================================
# ORDINE
# ========================================================

ordine = np.argsort(differenze)

termini_ordinati = [
    termini[i]
    for i in ordine
]

differenze_ordinate = [
    differenze[i]
    for i in ordine
]


# ========================================================
# GRAFICO
# ========================================================

plt.figure(figsize=(10, 7))

barre = plt.barh(
    termini_ordinati,
    differenze_ordinate
)

plt.axvline(
    0,
    linewidth=1
)

for barra, valore in zip(
    barre,
    differenze_ordinate
):

    if valore >= 0:
        x = valore + 0.2
        ha = "left"
    else:
        x = valore - 0.2
        ha = "right"

    plt.text(
        x,
        barra.get_y() + barra.get_height() / 2,
        str(valore),
        va="center",
        ha=ha,
        fontsize=10
    )


plt.title(
    "Differenza di frequenza dei termini di novità/attesa",
    fontsize=14
)

plt.xlabel(
    "Occorrenze Top 25 − occorrenze 26–100"
)

plt.tight_layout()

plt.savefig(
    "grafico_termini_novita.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
