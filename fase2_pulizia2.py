import pandas as pd
from google.colab import files


# ========================================================
# CARICAMENTO CSV FASE 2
# ========================================================

print("=" * 60)
print("CARICAMENTO DATASET FASE 2")
print("=" * 60)

caricati = files.upload()

if not caricati:
    raise FileNotFoundError(
        "Nessun file è stato caricato."
    )

nome_file = list(caricati.keys())[0]

print(
    f"\n✅ File utilizzato: {nome_file}"
)


# ========================================================
# LETTURA DEL CSV
# ========================================================

df = pd.read_csv(
    nome_file,
    sep=";",
    encoding="utf-8-sig"
)

print(
    "\nNumero libri:",
    len(df)
)


# ========================================================
# RIMOZIONE DELLA PAROLA "DESCRIZIONE"
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
# CONTROLLO
# ========================================================

print("\nControllo prime 3 descrizioni:\n")

for i, testo in enumerate(
    df["descrizione"].head(3),
    start=1
):

    print(f"--- DESCRIZIONE {i} ---")
    print(testo)
    print()


# ========================================================
# CONTROLLO EVENTUALI "DESCRIZIONE" RESIDUE
# ========================================================

residue = (
    df["descrizione"]
    .str.match(
        r"^\s*Descrizione\b",
        case=False,
        na=False
    )
    .sum()
)

print(
    "Descrizioni che iniziano ancora con "
    "'Descrizione':",
    residue
)


# ========================================================
# SALVATAGGIO FASE 3
# ========================================================

nome_output = "classifica_ibs_fase3.csv"

df.to_csv(
    nome_output,
    index=False,
    sep=";",
    encoding="utf-8-sig"
)

print(
    f"\n✅ File salvato come: {nome_output}"
)


# ========================================================
# CONTROLLO FILE FINALE
# ========================================================

df_controllo = pd.read_csv(
    nome_output,
    sep=";",
    encoding="utf-8-sig"
)

print("\n")
print("=" * 60)
print("CONTROLLO FINALE")
print("=" * 60)

print(
    "Numero righe:",
    len(df_controllo)
)

print(
    "Numero colonne:",
    len(df_controllo.columns)
)

print(
    "Colonne:",
    df_controllo.columns.tolist()
)


# ========================================================
# DOWNLOAD
# ========================================================

files.download(
    nome_output
)
