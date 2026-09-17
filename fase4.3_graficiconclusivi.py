# ============================================================
# ANALISI DEL LINGUAGGIO PROMOZIONALE PER GENERE
# ============================================================

import pandas as pd
import re
import numpy as np

# ------------------------------------------------------------
# 1. CARICAMENTO DEL DATASET FINALE
# ------------------------------------------------------------

nome_file = "classifica_ibs_fase2 pulita 07.09.csv" # Changed to load the available cleaned file

df = pd.read_csv(nome_file, sep=";", encoding="utf-8-sig") # Added sep parameter to match previous saves

# Added the cleaning step from the interrupted cell 'aXquwOZpWt3u'
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

print("Dataset caricato correttamente.")
print("Numero di libri:", len(df))
print("Colonne presenti:")
print(df.columns.tolist())


# ------------------------------------------------------------
# 2. CONTROLLO DELLE COLONNE NECESSARIE
# ------------------------------------------------------------

colonne_necessarie = [
    "posizione",
    "titolo",
    "categoria",
    "descrizione"
]

mancanti = [col for col in colonne_necessarie if col not in df.columns]

if mancanti:
    raise ValueError(
        f"Nel dataset mancano queste colonne: {mancanti}"
    )

print("\nTutte le colonne necessarie sono presenti.")


# ------------------------------------------------------------
# 3. PULIZIA DELLA DESCRIZIONE
# ------------------------------------------------------------

df["descrizione"] = df["descrizione"].fillna("").astype(str)

# Uniformiamo minuscole e spazi
df["testo_analisi"] = (
    df["descrizione"]
    .str.lower()
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)


# ------------------------------------------------------------
# 4. DIZIONARI FINALI DELLE 4 CATEGORIE
#    (quelli già definiti e congelati nella Fase 3)
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# 5. FUNZIONE PER CONTARE LE OCCORRENZE
# ------------------------------------------------------------

def conta_termini(testo, lista_termini):
    """
    Conta quante volte compaiono i termini della categoria.
    Per le espressioni composte vengono considerate le occorrenze
    della frase completa.
    """

    testo = testo.lower()

    totale = 0

    for termine in lista_termini:
        termine = termine.lower()

        # \b permette di evitare conteggi dentro parole più lunghe
        pattern = r"\b" + re.escape(termine) + r"\b"

        totale += len(re.findall(pattern, testo))

    return totale


# ------------------------------------------------------------
# 6. NUMERO DI PAROLE
# ------------------------------------------------------------

def conta_parole(testo):
    if not testo.strip():
        return 0

    return len(re.findall(r"\b[\wÀ-ÿ'-]+\b", testo))


df["numero_parole"] = df["testo_analisi"].apply(conta_parole)


# ------------------------------------------------------------
# 7. CONTEGGIO DELLE 4 CATEGORIE
# ------------------------------------------------------------

df["valutativi_positivi"] = df["testo_analisi"].apply(
    lambda x: conta_termini(x, valutativi_positivi)
)

df["premi_riconoscimenti"] = df["testo_analisi"].apply(
    lambda x: conta_termini(x, premi_riconoscimenti)
)

df["novita_attesa"] = df["testo_analisi"].apply(
    lambda x: conta_termini(x, novita_attesa)
)

df["coinvolgimento_lettore"] = df["testo_analisi"].apply(
    lambda x: conta_termini(x, coinvolgimento_lettore)
)


# ------------------------------------------------------------
# 8. NORMALIZZAZIONE: OCCORRENZE OGNI 100 PAROLE
# ------------------------------------------------------------

categorie_linguistiche = [
    "valutativi_positivi",
    "premi_riconoscimenti",
    "novita_attesa",
    "coinvolgimento_lettore"
]

for col in categorie_linguistiche:
    nuova_colonna = col + "_per_100_parole"

    df[nuova_colonna] = np.where(
        df["numero_parole"] > 0,
        df[col] / df["numero_parole"] * 100,
        np.nan
    )


# ------------------------------------------------------------
# 9. SELEZIONE DELLE COLONNE UTILI
# ------------------------------------------------------------

df_genere = df[
    [
        "posizione",
        "titolo",
        "categoria",
        "numero_parole",

        "valutativi_positivi",
        "premi_riconoscimenti",
        "novita_attesa",
        "coinvolgimento_lettore",

        "valutativi_positivi_per_100_parole",
        "premi_riconoscimenti_per_100_parole",
        "novita_attesa_per_100_parole",
        "coinvolgimento_lettore_per_100_parole"
    ]
].copy()


# ------------------------------------------------------------
# 10. CONTROLLO DEI GENERI
# ------------------------------------------------------------

print("\n" + "="*60)
print("LIBRI PER GENERE")
print("="*60)

print(
    df_genere["categoria"]
    .value_counts(dropna=False)
)


# ------------------------------------------------------------
# 11. TABELLA RIASSUNTIVA PER GENERE
# ------------------------------------------------------------

riassunto_generi = (
    df_genere
    .groupby("categoria", dropna=False)
    .agg(
        numero_libri=("titolo", "count"),

        media_valutativi=(
            "valutativi_positivi_per_100_parole",
            "mean"
        ),

        media_premi=(
            "premi_riconoscimenti_per_100_parole",
            "mean"
        ),

        media_novita=(
            "novita_attesa_per_100_parole",
            "mean"
        ),

        media_coinvolgimento=(
            "coinvolgimento_lettore_per_100_parole",
            "mean"
        )
    )
    .reset_index()
)


# Arrotondamento
colonne_numeriche = [
    "media_valutativi",
    "media_premi",
    "media_novita",
    "media_coinvolgimento"
]

riassunto_generi[colonne_numeriche] = (
    riassunto_generi[colonne_numeriche]
    .round(3)
)


print("\n" + "="*60)
print("MEDIA DEL LINGUAGGIO PROMOZIONALE PER GENERE")
print("="*60)

display(riassunto_generi)


# ------------------------------------------------------------
# 12. SALVATAGGIO DEI DATI
# ------------------------------------------------------------

df_genere.to_csv(
    "linguaggio_promozionale_per_genere.csv",
    index=False,
    encoding="utf-8-sig"
)

riassunto_generi.to_csv(
    "riassunto_linguaggio_per_genere.csv",
    index=False,
    encoding="utf-8-sig"
)


print("\nFile creati:")
print("1. linguaggio_promozionale_per_genere.csv")
print("2. riassunto_linguaggio_per_genere.csv")

# ============================================================
# LINGUAGGIO PROMOZIONALE E MACRO-GENERE
# Heatmap + grafico a barre
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ------------------------------------------------------------
# 1. CARICAMENTO DATI
# ------------------------------------------------------------

file = "linguaggio_promozionale_per_genere.csv"

df = pd.read_csv(file, encoding="utf-8-sig")

print("Dataset caricato.")
print("Numero di libri:", len(df))


# ------------------------------------------------------------
# 2. CREAZIONE DELLE MACRO-CATEGORIE
# ------------------------------------------------------------

def assegna_macro_genere(categoria):

    if pd.isna(categoria):
        return None

    # NARRATIVA
    if categoria in [
        "Narrativa italiana",
        "Narrativa straniera",
        "Gialli, thriller, horror",
        "Narrativa erotica e rosa"
    ]:
        return "Narrativa"

    # BAMBINI
    elif categoria == "Bambini e ragazzi":
        return "Bambini e ragazzi"

    # SAGGISTICA E CULTURA
    elif categoria in [
        "Società, politica e comunicazione",
        "Biografie",
        "Filosofia",
        "Storia e archeologia",
        "Arte, architettura e fotografia",
        "Cinema, musica, tv, spettacolo",
        "Educazione e formazione",
        "Classici, poesia, teatro e critica",
        "Religione e spiritualità"
    ]:
        return "Saggistica e cultura"

    # SCIENZE / SALUTE
    elif categoria in [
        "Medicina",
        "Scienze, geografia, ambiente",
        "Salute, famiglia e benessere personale"
    ]:
        return "Scienze e salute"

    # CASA / TEMPO LIBERO
    elif categoria == "Casa, hobby e cucina":
        return "Casa e tempo libero"

    else:
        return "Altro"


df["macro_genere"] = df["categoria"].apply(assegna_macro_genere)


# ------------------------------------------------------------
# 3. CONTROLLO DEL NUMERO DI LIBRI PER MACRO-GENERE
# ------------------------------------------------------------

print("\n" + "="*60)
print("LIBRI PER MACRO-GENERE")
print("="*60)

print(
    df["macro_genere"]
    .value_counts(dropna=False)
)


# ------------------------------------------------------------
# 4. ELIMINIAMO IL LIBRO SENZA CATEGORIA
# ------------------------------------------------------------

df_analisi = df.dropna(subset=["macro_genere"]).copy()

print("\nLibri utilizzati nell'analisi:", len(df_analisi))


# ------------------------------------------------------------
# 5. MEDIA DELLE 4 CATEGORIE PER MACRO-GENERE
# ------------------------------------------------------------

colonne_linguistiche = {
    "valutativi_positivi_per_100_parole": "Valutativi positivi",
    "premi_riconoscimenti_per_100_parole": "Premi / riconoscimenti / successo",
    "novita_attesa_per_100_parole": "Novità / attesa",
    "coinvolgimento_lettore_per_100_parole": "Coinvolgimento del lettore"
}

tabella = (
    df_analisi
    .groupby("macro_genere")[
        list(colonne_linguistiche.keys())
    ]
    .mean()
    .rename(columns=colonne_linguistiche)
)

tabella = tabella.round(3)

print("\n" + "="*60)
print("LINGUAGGIO PROMOZIONALE MEDIO PER MACRO-GENERE")
print("="*60)

display(tabella)


# ============================================================
# 6. HEATMAP
# ============================================================

plt.figure(figsize=(11, 6))

sns.heatmap(
    tabella,
    annot=True,
    fmt=".3f",
    cmap="YlOrRd",
    linewidths=0.5
)

plt.title(
    "Presenza del linguaggio promozionale per macro-genere",
    fontsize=14
)

plt.xlabel("Categoria di linguaggio promozionale")
plt.ylabel("Macro-genere")

plt.tight_layout()

plt.savefig(
    "heatmap_linguaggio_macro_genere.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 7. GRAFICO A BARRE
# ============================================================

# Trasformiamo la tabella in formato lungo
grafico = (
    tabella
    .reset_index()
    .melt(
        id_vars="macro_genere",
        var_name="categoria_linguistica",
        value_name="occorrenze_per_100_parole"
    )
)

plt.figure(figsize=(13, 7))

sns.barplot(
    data=grafico,
    x="macro_genere",
    y="occorrenze_per_100_parole",
    hue="categoria_linguistica"
)

plt.title(
    "Linguaggio promozionale medio per macro-genere",
    fontsize=14
)

plt.xlabel("Macro-genere")
plt.ylabel("Occorrenze ogni 100 parole")

plt.xticks(rotation=15)

plt.legend(
    title="Categoria linguistica",
    bbox_to_anchor=(1.02, 1),
    loc="upper left"
)

plt.tight_layout()

plt.savefig(
    "barplot_linguaggio_macro_genere.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# ============================================================
# 8. SALVATAGGIO DELLA TABELLA
# ============================================================

tabella.to_csv(
    "linguaggio_promozionale_macro_generi.csv",
    encoding="utf-8-sig"
)

print("\nFile creati:")
print("- heatmap_linguaggio_macro_genere.png")
print("- barplot_linguaggio_macro_genere.png")
print("- linguaggio_promozionale_macro_generi.csv")
