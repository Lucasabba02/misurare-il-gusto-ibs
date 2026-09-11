from google.colab import files

caricati = files.upload()
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


def conta_frasi(testo):

    if pd.isna(testo):
        return 0

    return len(
        re.findall(
            r"[.!?]+(?=\s|$)",
            str(testo)
        )
    )


def conta_domande(testo):

    if pd.isna(testo):
        return 0

    return str(testo).count("?")


def conta_citazioni(testo):

    if pd.isna(testo):
        return 0

    # Conta le sequenze racchiuse tra virgolette
    citazioni = re.findall(
        r"[«“\"](.+?)[»”\"]",
        str(testo)
    )

    return len(citazioni)


def presenza_premi(testo):

    if pd.isna(testo):
        return 0

    pattern = (
        r"\bpremio\b|"
        r"\bpremiata\b|"
        r"\bpremiato\b|"
        r"\bvincitore\b|"
        r"\bvincitrice\b|"
        r"\bfinalista\b|"
        r"\bfinalisti\b|"
        r"\bcandidato\b|"
        r"\bcandidata\b|"
        r"\bselezionato\b|"
        r"\bselezionata\b|"
        r"\bbestseller\b|"
        r"\bbest seller\b"
    )

    return int(
        bool(
            re.search(
                pattern,
                str(testo),
                flags=re.IGNORECASE
            )
        )
    )


def presenza_argomenti(testo):

    if pd.isna(testo):
        return 0

    return int(
        bool(
            re.search(
                r"\bArgomenti\b",
                str(testo),
                flags=re.IGNORECASE
            )
        )
    )


# ========================================================
# CREAZIONE DELLE FEATURE
# ========================================================

df["numero_parole"] = (
    df["descrizione"]
    .apply(conta_parole)
)

df["numero_caratteri"] = (
    df["descrizione"]
    .fillna("")
    .astype(str)
    .str.len()
)

df["numero_frasi"] = (
    df["descrizione"]
    .apply(conta_frasi)
)

df["numero_domande"] = (
    df["descrizione"]
    .apply(conta_domande)
)

df["numero_citazioni"] = (
    df["descrizione"]
    .apply(conta_citazioni)
)

df["presenza_premi"] = (
    df["descrizione"]
    .apply(presenza_premi)
)

df["presenza_argomenti"] = (
    df["descrizione"]
    .apply(presenza_argomenti)
)


# ========================================================
# TABELLA RIASSUNTIVA
# ========================================================

feature = [
    "numero_parole",
    "numero_caratteri",
    "numero_frasi",
    "numero_domande",
    "numero_citazioni",
    "presenza_premi",
    "presenza_argomenti"
]

print("=" * 60)
print("ANALISI ESPLORATIVA")
print("=" * 60)

print(
    df[feature].describe().round(2)
)


# ========================================================
# CONTEGGI DELLE VARIABILI BINARIE
# ========================================================

print("\n")
print("=" * 60)
print("PRESENZA DI ELEMENTI PROMOZIONALI")
print("=" * 60)

print(
    "Libri con premi/riconoscimenti:",
    int(df["presenza_premi"].sum())
)

print(
    "Libri con Argomenti:",
    int(df["presenza_argomenti"].sum())
)


# ========================================================
# CORRELAZIONI CON LA POSIZIONE
# ========================================================

print("\n")
print("=" * 60)
print("CORRELAZIONI CON LA POSIZIONE IN CLASSIFICA")
print("=" * 60)

for variabile in feature:

    correlazione = df[
        ["posizione", variabile]
    ].corr().iloc[0, 1]

    print(
        f"{variabile}: {correlazione:.3f}"
    )


# ========================================================
# LIBRI NELLA TOP 10
# ========================================================

print("\n")
print("=" * 60)
print("TOP 10")
print("=" * 60)

print(
    df[
        [
            "posizione",
            "titolo",
            "numero_parole",
            "numero_frasi",
            "numero_domande",
            "numero_citazioni",
            "presenza_premi",
            "presenza_argomenti"
        ]
    ]
    .head(10)
    .to_string(index=False)


    # ========================================================
# CONFRONTO TRA FASCE DI CLASSIFICA
# ========================================================

fasce = {
    "Top 10": (1, 10),
    "Top 25": (1, 25),
    "Centro": (26, 75),
    "Fondo": (76, 100)
}


# ========================================================
# VARIABILI DA CONFRONTARE
# ========================================================

variabili = [
    "numero_parole",
    "numero_caratteri",
    "numero_frasi",
    "numero_domande",
    "numero_citazioni",
    "presenza_premi",
    "presenza_argomenti"
]


# ========================================================
# CALCOLO DELLE MEDIE
# ========================================================

risultati = []

for nome_fascia, intervallo in fasce.items():

    minimo = intervallo[0]
    massimo = intervallo[1]

    sottoinsieme = df[
        (df["posizione"] >= minimo) &
        (df["posizione"] <= massimo)
    ]

    riga = {
        "fascia": nome_fascia,
        "libri": len(sottoinsieme)
    }

    for variabile in variabili:

        riga[variabile] = (
            sottoinsieme[variabile]
            .mean()
        )

    risultati.append(riga)


# ========================================================
# DATAFRAME RISULTATI
# ========================================================

df_fasce = pd.DataFrame(
    risultati
)


# ========================================================
# ARROTONDAMENTO
# ========================================================

df_fasce[
    variabili
] = df_fasce[
    variabili
].round(2)


# ========================================================
# VISUALIZZAZIONE
# ========================================================

print("=" * 60)
print("CONFRONTO TRA FASCE DI CLASSIFICA")
print("=" * 60)

print(
    df_fasce.to_string(
        index=False
    )
)


# ========================================================
# PERCENTUALI PER PREMI E ARGOMENTI
# ========================================================

print("\n")
print("=" * 60)
print("PERCENTUALE DI LIBRI CON ELEMENTI PROMOZIONALI")
print("=" * 60)

for nome_fascia, intervallo in fasce.items():

    minimo = intervallo[0]
    massimo = intervallo[1]

    sottoinsieme = df[
        (df["posizione"] >= minimo) &
        (df["posizione"] <= massimo)
    ]

    percentuale_premi = (
        sottoinsieme["presenza_premi"].mean()
        * 100
    )

    percentuale_argomenti = (
        sottoinsieme["presenza_argomenti"].mean()
        * 100
    )

    print(
        f"{nome_fascia}: "
        f"premi {percentuale_premi:.1f}% | "
        f"Argomenti {percentuale_argomenti:.1f}%"
    )
)
