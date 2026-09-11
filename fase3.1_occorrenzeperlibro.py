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
# DIZIONARI DEFINITIVI
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

        # Per le espressioni con più parole
        # usiamo direttamente l'espressione.
        pattern = r"\b" + re.escape(termine.lower()) + r"\b"

        totale += len(
            re.findall(
                pattern,
                testo
            )
        )

    return totale


# ========================================================
# NUMERO DI PAROLE
# ========================================================

df["numero_parole"] = df["descrizione"].apply(
    conta_parole
)

denominatore = (
    df["numero_parole"]
    .replace(0, np.nan) # Changed pd.NA to np.nan
)


# ========================================================
# CALCOLO DELLE 4 CATEGORIE
# ========================================================

df["valutativi_positivi"] = df["descrizione"].apply(
    lambda x: conta_termini(
        x,
        valutativi_positivi
    )
)

df["premi_riconoscimenti"] = df["descrizione"].apply(
    lambda x: conta_termini(
        x,
        premi_riconoscimenti
    )
)

df["novita_attesa"] = df["descrizione"].apply(
    lambda x: conta_termini(
        x,
        novita_attesa
    )
)

df["coinvolgimento_lettore"] = df["descrizione"].apply(
    lambda x: conta_termini(
        x,
        coinvolgimento_lettore
    )
)


# ========================================================
# NORMALIZZAZIONE PER 100 PAROLE
# ========================================================

categorie = [
    "valutativi_positivi",
    "premi_riconoscimenti",
    "novita_attesa",
    "coinvolgimento_lettore"
]

for categoria in categorie:

    df[
        categoria + "_per_100_parole"
    ] = (
        df[categoria]
        / denominatore
        * 100
    )


# ========================================================
# RISULTATI GENERALI
# ========================================================

print("=" * 60)
print("LINGUAGGIO PROMOZIONALE - RISULTATI")
print("=" * 60)

for categoria in categorie:

    print(
        f"\n{categoria}"
    )

    print(
        "  Occorrenze totali:",
        int(df[categoria].sum())
    )

    print(
        "  Libri con almeno un'occorrenza:",
        int(
            (df[categoria] > 0).sum()
        )
    )


# ========================================================
# CORRELAZIONI
# ========================================================

print("\n")
print("=" * 60)
print("CORRELAZIONI CON LA POSIZIONE")
print("=" * 60)

for categoria in categorie:

    variabile = (
        categoria +
        "_per_100_parole"
    )

    correlazione = df[
        ["posizione", variabile]
    ].corr().iloc[0, 1]

    print(
        f"{variabile}: {correlazione:.3f}"
    )
