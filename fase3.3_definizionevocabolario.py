import pandas as pd
import re


# ========================================================
# CARICAMENTO DATASET
# ========================================================

df = pd.read_csv(
    "classifica_ibs_fase2 pulita 07.09.csv",
    sep=";",
    encoding="utf-8-sig"
)


# ========================================================
# DIZIONARI / PATTERN
# ========================================================

intensificatori = [
    "molto",
    "davvero",
    "assolutamente",
    "estremamente",
    "incredibilmente",
    "straordinariamente",
    "profondamente",
    "fortemente"
]

valutativi_positivi = [
    "straordinario",
    "straordinaria",
    "eccezionale",
    "eccezionali",
    "incredibile",
    "incredibili",
    "imperdibile",
    "imperdibili",
    "meraviglioso",
    "meravigliosa",
    "stupendo",
    "stupenda",
    "favoloso",
    "favolosa",
    "magnifico",
    "magnifica",
    "bellissimo",
    "bellissima",
    "capolavoro",
    "capolavori",
    "talento",
    "grande",
    "grandi",
    "importante",
    "importanti",
    "coinvolgente",
    "coinvolgenti",
    "appassionante",
    "appassionante",
    "emozionante",
    "emozionanti"
]

attrazione_novita = [
    "atteso",
    "attesissima",
    "attesissimo",
    "attesa",
    "novità",
    "nuovo",
    "nuova",
    "nuovi",
    "nuove",
    "fenomeno",
    "successo",
    "bestseller",
    "bestseller internazionale",
    "libro dell'anno",
    "romanzo dell'anno"
]


# ========================================================
# FUNZIONE GENERICA DI CONTEGGIO
# ========================================================

def conta_termini(testo, lista):

    if pd.isna(testo):
        return 0

    testo = str(testo).lower()

    totale = 0

    for termine in lista:

        # Conta anche occorrenze multiple
        pattern = r"\b" + re.escape(termine.lower()) + r"\b"

        totale += len(
            re.findall(
                pattern,
                testo
            )
        )

    return totale


def conta_domande(testo):

    if pd.isna(testo):
        return 0

    return str(testo).count("?")


# ========================================================
# FEATURE
# ========================================================

df["numero_intensificatori"] = df["descrizione"].apply(
    lambda x: conta_termini(x, intensificatori)
)

df["numero_valutativi_positivi"] = df["descrizione"].apply(
    lambda x: conta_termini(x, valutativi_positivi)
)

df["numero_attrazione_novita"] = df["descrizione"].apply(
    lambda x: conta_termini(x, attrazione_novita)
)

# Calcola 'numero_domande' prima di usarlo per 'presenza_domanda'
df["numero_domande"] = (
    df["descrizione"]
    .apply(conta_domande)
)

df["presenza_domanda"] = (
    df["numero_domande"] > 0
).astype(int)


# ========================================================
# RISULTATI GENERALI
# ========================================================

print("=" * 60)
print("ANALISI DEL LINGUAGGIO PROMOZIONALE")
print("=" * 60)

print(
    "\nTotale occorrenze di intensificatori:",
    df["numero_intensificatori"].sum()
)

print(
    "Totale occorrenze di valutativi positivi:",
    df["numero_valutativi_positivi"].sum()
)

print(
    "Totale occorrenze di formule di attrazione/novità:",
    df["numero_attrazione_novita"].sum()
)

print(
    "Libri con almeno una domanda:",
    df["presenza_domanda"].sum()
)


# ========================================================
# STATISTICHE
# ========================================================

feature_linguistiche = [
    "numero_intensificatori",
    "numero_valutativi_positivi",
    "numero_attrazione_novita",
    "presenza_domanda"
]

print("\n")
print("=" * 60)
print("STATISTICHE DESCRITTIVE")
print("=" * 60)

print(
    df[feature_linguistiche]
    .describe()
    .round(2)
)


# ========================================================
# CORRELAZIONI CON LA POSIZIONE
# ========================================================

print("\n")
print("=" * 60)
print("CORRELAZIONI CON LA POSIZIONE")
print("=" * 60)

for variabile in feature_linguistiche:

    correlazione = df[
        ["posizione", variabile]
    ].corr().iloc[0, 1]

    print(
        f"{variabile}: {correlazione:.3f}"
    )
