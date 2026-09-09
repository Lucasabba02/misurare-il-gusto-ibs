import pandas as pd
import re
from google.colab import files


# ========================================================
# CARICAMENTO CSV FASE 2
# ========================================================

nome_file = "classifica_ibs_fase2.csv"

df = pd.read_csv(
    nome_file,
    sep=";",
    encoding="utf-8-sig"
)

print("=" * 60)
print("PULIZIA DATASET FASE 2")
print("=" * 60)

print(
    "Numero di righe prima della pulizia:",
    len(df)
)


# ========================================================
# FUNZIONE DI PULIZIA
# ========================================================

def pulisci_descrizione(testo):

    if pd.isna(testo):
        return testo

    testo = str(testo)

    # Rimuove i testi dei pulsanti IBS
    testo = testo.replace(
        "Leggi di più",
        ""
    )

    testo = testo.replace(
        "Leggi di meno",
        ""
    )

    # Rimuove eventuali spazi multipli
    testo = re.sub(
        r"\s+",
        " ",
        testo
    )

    # Rimuove eventuali spazi prima/dopo
    testo = testo.strip()

    return testo


# ========================================================
# APPLICAZIONE DELLA PULIZIA
# ========================================================

df["descrizione"] = df["descrizione"].apply(
    pulisci_descrizione
)


# ========================================================
# CONTROLLO PRESENZA TESTI INTERFACCIA
# ========================================================

testi_interfaccia = (
    df["descrizione"]
    .fillna("")
    .str.contains(
        r"Leggi di più|Leggi di meno",
        case=False,
        regex=True
    )
)

numero_residuo = testi_interfaccia.sum()

print(
    "\nDescrizioni che contengono ancora "
    "'Leggi di più'/'Leggi di meno':",
    numero_residuo
)


# ========================================================
# CONTROLLO DESCRIZIONI MANCANTI
# ========================================================

descrizioni_mancanti = df["descrizione"].isna().sum()

print(
    "Descrizioni mancanti:",
    descrizioni_mancanti
)


# ========================================================
# CONTROLLO NUMERO RIGHE
# ========================================================

print(
    "Numero di righe dopo la pulizia:",
    len(df)
)


# ========================================================
# PRIME 3 DESCRIZIONI
# ========================================================

print("\nPrime 3 descrizioni dopo la pulizia:\n")

for i, descrizione in enumerate(
    df["descrizione"].head(3),
    start=1
):

    print(f"--- DESCRIZIONE {i} ---")

    print(descrizione)

    print()


# ========================================================
# SALVATAGGIO
# ========================================================

df.to_csv(
    nome_file,
    index=False,
    sep=";",
    encoding="utf-8-sig"
)

print(
    f"✅ File aggiornato: {nome_file}"
)


# ========================================================
# CONTROLLO FINALE DEL FILE
# ========================================================

df_controllo = pd.read_csv(
    nome_file,
    sep=";",
    encoding="utf-8-sig"
)

print("\n")
print("=" * 60)
print("CONTROLLO FINALE")
print("=" * 60)

print(
    "Righe:",
    len(df_controllo)
)

print(
    "Colonne:",
    len(df_controllo.columns)
)

print(
    "Nomi colonne:",
    df_controllo.columns.tolist()
)


if len(df_controllo) == 100:
    print(
        "✅ Il dataset contiene ancora 100 libri."
    )
else:
    print(
        "⚠️ ATTENZIONE: il dataset non contiene 100 righe."
    )


# ========================================================
# DOWNLOAD DEL CSV PULITO
# ========================================================

files.download(
    nome_file
)
