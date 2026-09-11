# ========================================================
# CONFRONTO TOP 25 VS RESTO DELLA CLASSIFICA
# ========================================================

import pandas as pd
import re
import numpy as np # Import numpy


# ========================================================
# CARICAMENTO DATASET
# ========================================================

df = pd.read_csv(
    "classifica_ibs_fase2 pulita 07.09.csv", # Load the available file
    sep=";",
    encoding="utf-8-sig"
)

# ========================================================
# RIMOZIONE DELLA PAROLA "DESCRIZIONE"
# (Applying the cleaning step intended for classifica_ibs_fase3)
# ========================================================

df["descrizione"] = (
    df["descrizione"]
    .fillna("")
    .str.replace(
        r"^\s*Descrizione\s*",
        "",
        regex=True,
        case=False
    )
    .str.strip()
)


# ========================================================
# DIZIONARI
# ========================================================

valutativi_positivi = [
    "capolavoro",
    "capolavori",
    "straordinario",
    "straordinaria",
    "magistrale",
    "avvincente",
    "sorprendente",
    "indimenticabile",
    "brillante",
    "meraviglioso",
    "meravigliosa",
    "emozionante",
    "incredibile",
    "favoloso",
    "magnifico",
    "bellissimo",
    "bellissima",
    "coinvolgente",
    "appassionante",
    "imperdibile"
]

premi_riconoscimenti = [
    "premio",
    "premi",
    "vincitore",
    "vincitrice",
    "finalista",
    "candidato",
    "candidata",
    "bestseller",
    "libro dell'anno",
    "romanzo dell'anno",
    "successo"
]

novita_attesa = [
    "nuovo",
    "nuova",
    "nuovi",
    "nuove",
    "novità",
    "atteso",
    "attesissima",
    "nuovo romanzo",
    "fenomeno",
    "nuova edizione",
    "appena uscito"
]

coinvolgimento_lettore = [
    "perdersi",
    "da leggere",
    "immergersi",
    "da amare",
    "scoprirete",
    "da divorare"
]


# ========================================================
# FUNZIONI
# ========================================================

def conta_parole(testo):

    if pd.isna(testo):
        return 0

    return len(
        re.findall(
            r"\b\w+\b",
            str(testo),
            flags=re.UNICODE
        )
    )


def conta_termini(testo, lista):

    if pd.isna(testo):
        return 0

    testo = str(testo).lower()

    totale = 0

    for termine in lista:

        pattern = (
            r"\b"
            + re.escape(termine.lower())
            + r"\b"
        )

        totale += len(
            re.findall(
                pattern,
                testo
            )
        )

    return totale


# ========================================================
# CALCOLO DELLE FEATURE
# ========================================================

df["numero_parole"] = (
    df["descrizione"]
    .apply(conta_parole)
)

denominatore = (
    df["numero_parole"]
    .replace(0, np.nan) # Changed pd.NA to np.nan
)

categorie = {
    "valutativi_positivi": valutativi_positivi,
    "premi_riconoscimenti": premi_riconoscimenti,
    "novita_attesa": novita_attesa,
    "coinvolgimento_lettore": coinvolgimento_lettore
}


for nome, dizionario in categorie.items():

    df[nome] = df["descrizione"].apply(
        lambda x: conta_termini(
            x,
            dizionario
        )
    )

    df[nome + "_per_100_parole"] = (
        df[nome]
        / denominatore
        * 100
    )


# ========================================================
# CREAZIONE DEI DUE GRUPPI
# ========================================================

top25 = df[
    df["posizione"] <= 25
]

resto = df[
    df["posizione"] >= 26
]


# ========================================================
# CONFRONTO
# ========================================================

feature = [
    "valutativi_positivi_per_100_parole",
    "premi_riconoscimenti_per_100_parole",
    "novita_attesa_per_100_parole",
    "coinvolgimento_lettore_per_100_parole"
]


risultati = []

for variabile in feature:

    risultati.append({
        "categoria": variabile,
        "Top 25": top25[variabile].mean(),
        "Posizioni 26-100": resto[variabile].mean()
    })


df_confronto = pd.DataFrame(
    risultati
)


df_confronto[
    ["Top 25", "Posizioni 26-100"]
] = df_confronto[
    ["Top 25", "Posizioni 26-100"]
].round(3)


# ========================================================
# OUTPUT
# ========================================================

print("=" * 60)
print("TOP 25 VS POSIZIONI 26-100")
print("=" * 60)

print(
    df_confronto.to_string(
        index=False
    )
)
