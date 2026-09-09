import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import io
import time
from google.colab import files


# ========================================================
# 1. CARICAMENTO DATASET DELLA FASE 1
# ========================================================

print("=" * 60)
print("CARICAMENTO DATASET FASE 1")
print("=" * 60)

caricati = files.upload()

if not caricati:
    raise FileNotFoundError(
        "Nessun file è stato caricato."
    )

nome_file_fase1 = list(caricati.keys())[0]

print(
    f"\n✅ File utilizzato: {nome_file_fase1}"
)


# ========================================================
# 2. LETTURA ROBUSTA DEL CSV
# ========================================================

print("\nLettura del dataset...")


# Prima prova con la lettura normale
df_fase1 = pd.read_csv(
    nome_file_fase1,
    encoding="utf-8-sig"
)


# ========================================================
# 3. CONTROLLO DELLA LETTURA
# ========================================================

colonne_attese = [
    "posizione",
    "titolo",
    "autore",
    "url",
    "rating",
    "numero_recensioni",
    "categoria",
    "editore_anno"
]


# Se il dataset è stato letto correttamente,
# lo utilizziamo direttamente.
lettura_corretta = (
    all(
        colonna in df_fase1.columns
        for colonna in colonne_attese
    )
    and
    df_fase1["url"].notna().sum() > 0
)


# ========================================================
# 4. RECUPERO DI UN EVENTUALE CSV MALFORMATO
# ========================================================

if not lettura_corretta:

    print(
        "\n⚠️ Il CSV non è stato interpretato "
        "correttamente."
    )

    print(
        "Tentativo di ricostruzione automatica..."
    )


    # ----------------------------------------------------
    # Lettura del file come testo
    # ----------------------------------------------------

    with open(
        nome_file_fase1,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        testo = file.read()


    # ----------------------------------------------------
    # Separazione delle righe
    # ----------------------------------------------------

    lettore = csv.reader(
        io.StringIO(testo),
        delimiter=",",
        quotechar='"'
    )

    righe = list(lettore)


    # ----------------------------------------------------
    # Controllo intestazione
    # ----------------------------------------------------

    intestazione = righe[0]

    print(
        "\nIntestazione trovata:"
    )

    print(
        intestazione
    )


    # ----------------------------------------------------
    # Ricostruzione delle righe
    # ----------------------------------------------------

    righe_corrette = []

    for riga in righe[1:]:

        # Ignora righe vuote
        if not riga:
            continue


        # Caso normale:
        # la riga contiene già tutte le colonne
        if len(riga) == 8:

            righe_corrette.append(riga)

            continue


        # Caso problematico:
        # tutta la riga è stata salvata
        # come un unico campo.
        if len(riga) == 1:

            contenuto = riga[0]

            lettura_interna = csv.reader(
                io.StringIO(contenuto),
                delimiter=",",
                quotechar='"'
            )

            riga_ricostruita = next(
                lettura_interna
            )

            if len(riga_ricostruita) == 8:

                righe_corrette.append(
                    riga_ricostruita
                )

            else:

                print(
                    "⚠️ Riga non ricostruibile:",
                    contenuto[:100]
                )


    # ----------------------------------------------------
    # Creazione DataFrame ricostruito
    # ----------------------------------------------------

    df_fase1 = pd.DataFrame(
        righe_corrette,
        columns=colonne_attese
    )


# ========================================================
# 5. CONVERSIONE DELLE COLONNE NUMERICHE
# ========================================================

df_fase1["posizione"] = pd.to_numeric(
    df_fase1["posizione"],
    errors="coerce"
)

df_fase1["rating"] = pd.to_numeric(
    df_fase1["rating"],
    errors="coerce"
)

df_fase1["numero_recensioni"] = pd.to_numeric(
    df_fase1["numero_recensioni"],
    errors="coerce"
)


# ========================================================
# 6. RIMOZIONE EVENTUALI RIGHE NON VALIDE
# ========================================================

df_fase1 = df_fase1[
    df_fase1["posizione"].notna()
].copy()


df_fase1 = df_fase1.sort_values(
    "posizione"
).reset_index(drop=True)


# ========================================================
# 7. CONTROLLO DATASET
# ========================================================

print("\n")
print("=" * 60)
print("CONTROLLO DATASET FASE 1")
print("=" * 60)

print(
    "Numero libri presenti:",
    len(df_fase1)
)

print(
    "\nColonne:"
)

print(
    df_fase1.columns.tolist()
)


# Controllo URL
url_presenti = (
    df_fase1["url"]
    .notna()
    .sum()
)

print(
    "\nURL presenti:",
    url_presenti
)


if len(df_fase1) == 100:

    print(
        "✅ Il dataset contiene 100 libri."
    )

else:

    print(
        f"⚠️ Il dataset contiene "
        f"{len(df_fase1)} libri."
    )


if url_presenti == 100:

    print(
        "✅ Tutti i 100 libri hanno un URL."
    )

else:

    print(
        "⚠️ Alcuni URL risultano mancanti."
    )


# ========================================================
# 8. CONTROLLO DI UNA RIGA
# ========================================================

print("\n")
print("=" * 60)
print("PRIMO LIBRO")
print("=" * 60)

print(
    "Posizione:",
    df_fase1.iloc[0]["posizione"]
)

print(
    "Titolo:",
    df_fase1.iloc[0]["titolo"]
)

print(
    "Autore:",
    df_fase1.iloc[0]["autore"]
)

print(
    "URL:",
    df_fase1.iloc[0]["url"]
)


# ========================================================
# 9. IMPOSTAZIONI SCRAPING
# ========================================================

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0 Safari/537.36"
    )
}


# ========================================================
# 10. RACCOLTA DELLE DESCRIZIONI
# ========================================================

descrizioni = []

print("\n")
print("=" * 60)
print("INIZIO RACCOLTA DESCRIZIONI")
print("=" * 60)


for indice, riga in df_fase1.iterrows():

    posizione = riga["posizione"]
    titolo = riga["titolo"]
    url_libro = riga["url"]

    print("\n" + "-" * 60)

    print(
        f"Libro {indice + 1}/{len(df_fase1)}"
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

        print(
            "⚠️ URL mancante."
        )

        descrizioni.append(None)

        continue


    # ----------------------------------------------------
    # RICHIESTA PAGINA IBS
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
            "⚠️ Errore richiesta:",
            errore
        )

        descrizioni.append(None)

        time.sleep(2)

        continue


    # ----------------------------------------------------
    # CONTROLLO RISPOSTA
    # ----------------------------------------------------

    if risposta.status_code != 200:

        print(
            "⚠️ Pagina non disponibile."
        )

        descrizioni.append(None)

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
    # SEZIONE DESCRIZIONE
    # ----------------------------------------------------

    elemento_descrizione = soup.select_one(
        "#pdp-descrizione"
    )


    if elemento_descrizione:

        # In questa fase NON facciamo alcuna pulizia.
        # Raccogliamo il testo così come presente
        # nella sezione HTML "Descrizione".

        descrizione = elemento_descrizione.get_text(
            " ",
            strip=True
        )

        print(
            "✅ Descrizione trovata."
        )

    else:

        descrizione = None

        print(
            "⚠️ Descrizione NON trovata."
        )


    descrizioni.append(
        descrizione
    )


    # ----------------------------------------------------
    # PAUSA
    # ----------------------------------------------------

    time.sleep(2)


# ========================================================
# 11. CREAZIONE DATASET FASE 2
# ========================================================

df_fase2 = df_fase1.copy()

df_fase2["descrizione"] = descrizioni


# ========================================================
# 12. ORDINE COLONNE
# ========================================================

colonne_fase2 = [
    "posizione",
    "titolo",
    "autore",
    "url",
    "rating",
    "numero_recensioni",
    "categoria",
    "editore_anno",
    "descrizione"
]

df_fase2 = df_fase2[
    colonne_fase2
]


# ========================================================
# 13. ORDINAMENTO
# ========================================================

df_fase2 = df_fase2.sort_values(
    "posizione"
).reset_index(drop=True)


# ========================================================
# 14. CONTROLLO FINALE
# ========================================================

print("\n")
print("=" * 60)
print("CONTROLLO FINALE FASE 2")
print("=" * 60)

print(
    "Numero libri:",
    len(df_fase2)
)

print(
    "Numero colonne:",
    len(df_fase2.columns)
)

print(
    "\nColonne:"
)

print(
    df_fase2.columns.tolist()
)


# ========================================================
# 15. CONTROLLO DESCRIZIONI
# ========================================================

descrizioni_presenti = (
    df_fase2["descrizione"]
    .notna()
    .sum()
)

descrizioni_mancanti = (
    df_fase2["descrizione"]
    .isna()
    .sum()
)

print(
    "\nDescrizioni raccolte:",
    descrizioni_presenti
)

print(
    "Descrizioni mancanti:",
    descrizioni_mancanti
)


# ========================================================
# 16. CONTROLLO POSIZIONI
# ========================================================

posizioni_attese = set(
    range(1, 101)
)

posizioni_trovate = set(
    df_fase2["posizione"]
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
# 17. VALORI MANCANTI
# ========================================================

print(
    "\nValori mancanti per colonna:"
)

print(
    df_fase2.isna().sum()
)


# ========================================================
# 18. PRIME 3 RIGHE
# ========================================================

print("\n")
print("=" * 60)
print("PRIME 3 RIGHE")
print("=" * 60)

print(
    df_fase2.head(3).to_string(
        index=False
    )
)


# ========================================================
# 19. SALVATAGGIO CSV
# ========================================================

nome_file_output = "classifica_ibs_fase2.csv"

df_fase2.to_csv(
    nome_file_output,
    index=False,
    sep=";",
    encoding="utf-8-sig"
)

print(
    f"\n✅ File salvato come: {nome_file_output}"
)


# ========================================================
# 20. CONTROLLO CSV SALVATO
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
    and len(df_controllo.columns) == 9
):

    print(
        "\n✅ DATASET FASE 2 CREATO CORRETTAMENTE."
    )

else:

    print(
        "\n⚠️ ATTENZIONE: controllare il dataset."
    )


# ========================================================
# 21. DOWNLOAD
# ========================================================

print("\n")
print("=" * 60)
print("DOWNLOAD")
print("=" * 60)

files.download(
    nome_file_output
)
