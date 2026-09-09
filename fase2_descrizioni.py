import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from google.colab import files


# ========================================================
# 1. CARICAMENTO DEL CSV DELLA FASE 1
# ========================================================

print("=" * 60)
print("CARICAMENTO DATASET FASE 1")
print("=" * 60)

# Se il file non è ancora presente in Colab,
# questa finestra permette di caricarlo.
caricati = files.upload()

nome_file_fase1 = "classifica_ibs_fase1.csv"

if nome_file_fase1 not in caricati:
    print(
        f"\n⚠️ ATTENZIONE: non è stato trovato "
        f"'{nome_file_fase1}'."
    )
else:
    print(
        f"\n✅ File '{nome_file_fase1}' caricato correttamente."
    )


# ========================================================
# 2. LETTURA DEL CSV
# ========================================================

df_fase1 = pd.read_csv(
    nome_file_fase1,
    encoding="utf-8-sig"
)

print(
    "\nNumero libri presenti nel dataset:",
    len(df_fase1)
)

print(
    "\nColonne presenti:"
)

print(
    df_fase1.columns.tolist()
)


# ========================================================
# 3. CONTROLLO DEI 100 LIBRI
# ========================================================

if len(df_fase1) == 100:

    print(
        "\n✅ Il dataset contiene esattamente 100 libri."
    )

else:

    print(
        f"\n⚠️ ATTENZIONE: il dataset contiene "
        f"{len(df_fase1)} libri invece di 100."
    )


# ========================================================
# 4. IMPOSTAZIONI SCRAPING
# ========================================================

BASE_URL = "https://www.ibs.it"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0 Safari/537.36"
    )
}


# ========================================================
# 5. FUNZIONE DI PULIZIA DELLA DESCRIZIONE
# ========================================================

def pulisci_descrizione(testo):

    if not testo:
        return None

    # Sostituisce spazi multipli, tab e ritorni a capo
    testo = re.sub(
        r"\s+",
        " ",
        testo
    )

    return testo.strip()


# ========================================================
# 6. RACCOLTA DELLE DESCRIZIONI
# ========================================================

risultati = []

print("\n")
print("=" * 60)
print("INIZIO RACCOLTA DESCRIZIONI")
print("=" * 60)


for indice, riga in df_fase1.iterrows():

    posizione = riga["posizione"]
    titolo = riga["titolo"]
    autore = riga["autore"]
    url_libro = riga["url"]

    print("\n" + "-" * 60)
    print(
        f"Libro {indice + 1}/100"
    )
    print(
        f"Posizione: {posizione}"
    )
    print(
        f"Titolo: {titolo}"
    )


    # ----------------------------------------------------
    # CONTROLLO URL
    # ----------------------------------------------------

    if pd.isna(url_libro) or not str(url_libro).strip():

        print("⚠️ URL mancante.")

        risultati.append({
            "posizione": posizione,
            "titolo": titolo,
            "autore": autore,
            "url": url_libro,
            "descrizione": None
        })

        continue


    # ----------------------------------------------------
    # RICHIESTA DELLA PAGINA
    # ----------------------------------------------------

    try:

        risposta = requests.get(
            str(url_libro),
            headers=headers,
            timeout=20
        )

        print(
            "Codice risposta:",
            risposta.status_code
        )

    except requests.RequestException as errore:

        print(
            "⚠️ Errore durante la richiesta:",
            errore
        )

        risultati.append({
            "posizione": posizione,
            "titolo": titolo,
            "autore": autore,
            "url": url_libro,
            "descrizione": None
        })

        time.sleep(2)

        continue


    # ----------------------------------------------------
    # CONTROLLO RISPOSTA
    # ----------------------------------------------------

    if risposta.status_code != 200:

        print(
            "⚠️ Pagina non disponibile."
        )

        risultati.append({
            "posizione": posizione,
            "titolo": titolo,
            "autore": autore,
            "url": url_libro,
            "descrizione": None
        })

        time.sleep(2)

        continue


    # ----------------------------------------------------
    # PARSING HTML
    # ----------------------------------------------------

    soup = BeautifulSoup(
        risposta.content,
        "html.parser"
    )


    # ----------------------------------------------------
    # RICERCA DELLA SEZIONE DESCRIZIONE
    # ----------------------------------------------------

    elemento_descrizione = soup.select_one(
        "#pdp-descrizione"
    )


    if elemento_descrizione:

        descrizione = elemento_descrizione.get_text(
            " ",
            strip=True
        )

        descrizione = pulisci_descrizione(
            descrizione
        )

        print(
            "✅ Descrizione trovata."
        )

    else:

        descrizione = None

        print(
            "⚠️ Descrizione NON trovata."
        )


    # ----------------------------------------------------
    # SALVATAGGIO RISULTATO
    # ----------------------------------------------------

    risultati.append({
        "posizione": posizione,
        "titolo": titolo,
        "autore": autore,
        "url": url_libro,
        "descrizione": descrizione
    })


    # ----------------------------------------------------
    # PAUSA TRA LE RICHIESTE
    # ----------------------------------------------------

    time.sleep(2)


# ========================================================
# 7. CREAZIONE DATAFRAME FASE 2
# ========================================================

df_descrizioni = pd.DataFrame(
    risultati
)


# ========================================================
# 8. ORDINAMENTO
# ========================================================

df_descrizioni = df_descrizioni.sort_values(
    "posizione"
).reset_index(drop=True)


# ========================================================
# 9. CONTROLLO FINALE
# ========================================================

print("\n")
print("=" * 60)
print("CONTROLLO FINALE FASE 2")
print("=" * 60)


print(
    "Numero totale di libri:",
    len(df_descrizioni)
)


descrizioni_mancanti = (
    df_descrizioni["descrizione"]
    .isna()
    .sum()
)


descrizioni_presenti = (
    df_descrizioni["descrizione"]
    .notna()
    .sum()
)


print(
    "Descrizioni raccolte:",
    descrizioni_presenti
)


print(
    "Descrizioni mancanti:",
    descrizioni_mancanti
)


# ========================================================
# 10. CONTROLLO POSIZIONI
# ========================================================

posizioni_attese = set(
    range(1, 101)
)

posizioni_trovate = set(
    df_descrizioni["posizione"]
)

posizioni_mancanti = sorted(
    posizioni_attese - posizioni_trovate
)


if not posizioni_mancanti:

    print(
        "✅ Tutte le posizioni da 1 a 100 sono presenti."
    )

else:

    print(
        "⚠️ Posizioni mancanti:",
        posizioni_mancanti
    )


# ========================================================
# 11. PRIME 5 RIGHE
# ========================================================

print("\n")
print("=" * 60)
print("PRIME 5 RIGHE")
print("=" * 60)

print(
    df_descrizioni[
        [
            "posizione",
            "titolo",
            "autore",
            "descrizione"
        ]
    ]
    .head(5)
    .to_string(index=False)
)


# ========================================================
# 12. SALVATAGGIO CSV
# ========================================================

nome_file_output = "classifica_ibs_fase2.csv"

df_descrizioni.to_csv(
    nome_file_output,
    index=False,
    sep=";",
    encoding="utf-8-sig"
)


print(
    f"\n✅ File salvato come: {nome_file_output}"
)


# ========================================================
# 13. CONTROLLO DEL CSV APPENA SALVATO
# ========================================================

df_controllo = pd.read_csv(
    nome_file_output,
    sep=";",
    encoding="utf-8-sig"
)


print("\n")
print("=" * 60)
print("CONTROLLO DEL CSV SALVATO")
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
    "Colonne:"
)

print(
    df_controllo.columns.tolist()
)


if (
    len(df_controllo) == 100
    and len(df_controllo.columns) == 5
):

    print(
        "\n✅ CSV Fase 2 creato correttamente."
    )

else:

    print(
        "\n⚠️ Controllare il file generato."
    )


# ========================================================
# 14. DOWNLOAD DEL CSV
# ========================================================

print("\n")
print("=" * 60)
print("DOWNLOAD")
print("=" * 60)

files.download(
    nome_file_output
)
