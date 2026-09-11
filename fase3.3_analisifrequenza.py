import pandas as pd
import re
from scipy.stats import mannwhitneyu
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

df["numero_parole"] = df["descrizione"].apply(
    conta_parole
)

denominatore = (
    df["numero_parole"].replace(0, np.nan) # Changed pd.NA to np.nan
)

categorie = {
    "Valutativi positivi": valutativi_positivi,
    "Premi / riconoscimenti / successo": premi_riconoscimenti,
    "Novità / attesa": novita_attesa,
    "Coinvolgimento del lettore": coinvolgimento_lettore
}


for nome, dizionario in categorie.items():

    nome_colonna = nome.lower()

    nome_colonna = (
        nome_colonna
        .replace(" / ", "_")
        .replace(" ", "_")
    )

    df[nome_colonna] = df["descrizione"].apply(
        lambda x: conta_termini(
            x,
            dizionario
        )
    )

    df[nome_colonna + "_per_100_parole"] = (
        df[nome_colonna]
        / denominatore
        * 100
    )


# ========================================================
# CREAZIONE DEI GRUPPI
# ========================================================

top25 = df[
    df["posizione"] <= 25
].copy()

resto = df[
    df["posizione"] >= 26
].copy()


# ========================================================
# MANN-WHITNEY U
# ========================================================

feature = [
    (
        "Valutativi positivi",
        "valutativi_positivi_per_100_parole"
    ),
    (
        "Premi / riconoscimenti / successo",
        "premi_riconoscimenti_successo_per_100_parole"
    ),
    (
        "Novità / attesa",
        "novità_attesa_per_100_parole" # Corrected 'novita' to 'novità'
    ),
    (
        "Coinvolgimento del lettore",
        "coinvolgimento_del_lettore_per_100_parole"
    )
]


risultati = []


for nome, variabile in feature:

    # Drop NaN values from both groups before performing the test
    gruppo_top = (
        top25[variabile]
        .dropna()
    )

    gruppo_resto = (
        resto[variabile]
        .dropna()
    )

    # Only perform the test if both groups have enough data
    if len(gruppo_top) > 0 and len(gruppo_resto) > 0:
        statistica_u, p_value = mannwhitneyu(
            gruppo_top,
            gruppo_resto,
            alternative="two-sided"
        )
    else:
        # Assign NaN or some indicator if no data to compare
        statistica_u, p_value = np.nan, np.nan

    risultati.append({
        "categoria": nome,
        "mediana_top25": gruppo_top.median(),
        "mediana_resto": gruppo_resto.median(),
        "media_top25": gruppo_top.mean(),
        "media_resto": gruppo_resto.mean(),
        "U": statistica_u,
        "p_value": p_value
    })


# ========================================================
# RISULTATI
# ========================================================

risultati_df = pd.DataFrame(
    risultati
)

risultati_df[
    [
        "mediana_top25",
        "mediana_resto",
        "media_top25",
        "media_resto",
        "U",
        "p_value"
    ]
] = risultati_df[
    [
        "mediana_top25",
        "mediana_resto",
        "media_top25",
        "media_resto",
        "U",
        "p_value"
    ]
].round(4)


print("=" * 60)
print("TEST MANN-WHITNEY U: TOP 25 VS RESTO")
print("=" * 60)

print(
    risultati_df.to_string(
        index=False
    )
)


# ========================================================
# INTERPRETAZIONE AUTOMATICA
# ========================================================

print("\n")
print("=" * 60)
print("INTERPRETAZIONE")
print("=" * 60)

for _, riga in risultati_df.iterrows():

    if riga["p_value"] < 0.05:

        significativita = "SIGNIFICATIVA"

    else:

        significativita = "NON significativa"

    print(
        f"{riga['categoria']}: "
        f"{significativita} "
        f"(p = {riga['p_value']:.4f})"
    )
