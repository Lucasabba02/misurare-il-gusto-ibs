import matplotlib.pyplot as plt

# ========================================================
# DATI DEL GRAFICO
# ========================================================

categorie = [
    "Valutativi positivi",
    "Premi / riconoscimenti / successo",
    "Novità / attesa",
    "Coinvolgimento del lettore"
]

correlazioni = [
    0.143,
    -0.117,
    -0.136,
    -0.210
]


# ========================================================
# CREAZIONE GRAFICO
# ========================================================

plt.figure(figsize=(10, 6))

barre = plt.barh(
    categorie,
    correlazioni
)

# Linea verticale dello zero
plt.axvline(
    0,
    linewidth=1
)

# Etichette numeriche
for barra, valore in zip(barre, correlazioni):

    if valore >= 0:
        posizione_x = valore + 0.008
        allineamento = "left"
    else:
        posizione_x = valore - 0.008
        allineamento = "right"

    plt.text(
        posizione_x,
        barra.get_y() + barra.get_height() / 2,
        f"{valore:.3f}",
        va="center",
        ha=allineamento,
        fontsize=11
    )


# ========================================================
# TITOLI
# ========================================================

plt.title(
    "Correlazione tra linguaggio promozionale e posizione in classifica",
    fontsize=14
)

plt.xlabel(
    "Correlazione con la posizione in classifica"
)

plt.ylabel(
    "Tipo di linguaggio"
)


# ========================================================
# LIMITI ASSE X
# ========================================================

plt.xlim(
    -0.25,
    0.20
)


# ========================================================
# LAYOUT
# ========================================================

plt.tight_layout()

plt.show()
