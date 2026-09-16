!pip install requests beautifulsoup4 pandas
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time


# ========================================================
# IMPOSTAZIONI
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
# FUNZIONE PER CORREGGERE EVENTUALE MOJIBAKE
# ========================================================

def correggi_encoding(testo):

    if not isinstance(testo, str):
        return testo

    # Caratteri tipici di un testo interpretato
    # con una codifica errata
    caratteri_sospetti = ("Ã", "Â", "â", "ð")

    # Se non ci sono caratteri sospetti,
    # lasciamo il testo completamente invariato
    if not any(c in testo for c in caratteri_sospetti):
        return testo

    try:
        corretto = testo.encode("latin1").decode("utf-8")

        # Controlliamo che la correzione abbia
        # effettivamente ridotto i caratteri sospetti
        sospetti_originali = sum(
            testo.count(c)
            for c in caratteri_sospetti
        )

        sospetti_corretti = sum(
            corretto.count(c)
            for c in caratteri_sospetti
        )

        if sospetti_corretti < sospetti_originali:
            return corretto

    except (UnicodeEncodeError, UnicodeDecodeError):
        pass

    return testo


# ========================================================
# SCRAPING DELLE TRE PAGINE
# ========================================================

libri = []


for pagina in [1, 2, 3]:

    url = f"{BASE_URL}/classifica/libri/1week/sold?page={pagina}"

    print("=" * 60)
    print(f"PAGINA {pagina}")
    print("=" * 60)

    risposta = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    print("Codice risposta:", risposta.status_code)

    if risposta.status_code != 200:
        print("ERRORE: pagina non disponibile.")
        continue

    # Leggiamo direttamente i byte della pagina.
    # Questo riduce il rischio di problemi di encoding.
    soup = BeautifulSoup(
        risposta.content,
        "html.parser"
    )

    schede = soup.select(
        "div.cc-product-list-item.cc-product-list-item--ranking"
    )

    print("Schede trovate:", len(schede))

    for scheda in schede:

        # ------------------------------------------------
        # POSIZIONE
        # ------------------------------------------------

        elemento_posizione = scheda.select_one(
            ".cc-position"
        )

        if elemento_posizione is None:
            continue

        testo_posizione = elemento_posizione.get_text(
            " ",
            strip=True
        )

        match = re.search(
            r"\d+",
            testo_posizione
        )

        if match is None:
            continue

        posizione = int(match.group())


        # ------------------------------------------------
        # TITOLO
        # ------------------------------------------------

        elemento_titolo = scheda.select_one(
            "a.cc-title"
        )

        titolo = (
            elemento_titolo.get_text(
                " ",
                strip=True
            )
            if elemento_titolo
            else None
        )

        titolo = correggi_encoding(titolo)


        # ------------------------------------------------
        # AUTORE
        # ------------------------------------------------

        elemento_autore = scheda.select_one(
            "a.cc-author-name"
        )

        autore = (
            elemento_autore.get_text(
                " ",
                strip=True
            )
            if elemento_autore
            else None
        )

        autore = correggi_encoding(autore)


        # ------------------------------------------------
        # URL
        # ------------------------------------------------

        url_libro = (
            elemento_titolo.get("href")
            if elemento_titolo
            else None
        )

        if url_libro and url_libro.startswith("/"):
            url_libro = BASE_URL + url_libro


        # ------------------------------------------------
        # RATING
        # ------------------------------------------------

        rating = None

        elemento_rating = scheda.select_one(
            ".cc-rating"
        )

        if elemento_rating:

            testo_rating = elemento_rating.get_text(
                " ",
                strip=True
            )

            match_rating = re.search(
                r"(\d+)\s*/\s*5",
                testo_rating
            )

            if match_rating:
                rating = int(
                    match_rating.group(1)
                )


        # ------------------------------------------------
        # NUMERO RECENSIONI
        # ------------------------------------------------

        numero_recensioni = None

        elemento_recensioni = scheda.select_one(
            ".cc-rating-number"
        )

        if elemento_recensioni:

            testo_recensioni = elemento_recensioni.get_text(
                " ",
                strip=True
            )

            testo_recensioni = (
                testo_recensioni
                .replace("(", "")
                .replace(")", "")
                .replace(".", "")
                .strip()
            )

            if testo_recensioni.isdigit():
                numero_recensioni = int(
                    testo_recensioni
                )


        # ------------------------------------------------
        # CATEGORIA
        # ------------------------------------------------

        elemento_categoria = scheda.select_one(
            ".cc-category"
        )

        categoria = (
            elemento_categoria.get_text(
                " ",
                strip=True
            )
            if elemento_categoria
            else None
        )

        categoria = correggi_encoding(categoria)


        # ------------------------------------------------
        # EDITORE + ANNO
        # ------------------------------------------------

        elemento_owner = scheda.select_one(
            ".cc-owner"
        )

        editore_anno = (
            elemento_owner.get_text(
                " ",
                strip=True
            )
            if elemento_owner
            else None
        )

        editore_anno = correggi_encoding(editore_anno)


        # ------------------------------------------------
        # SALVATAGGIO
        # ------------------------------------------------

        libri.append({
            "posizione": posizione,
            "titolo": titolo,
            "autore": autore,
            "url": url_libro,
            "rating": rating,
            "numero_recensioni": numero_recensioni,
            "categoria": categoria,
            "editore_anno": editore_anno
        })

        print(
            f"{posizione:>3} | "
            f"{titolo} | "
            f"{autore}"
        )

    time.sleep(2)


# ========================================================
# DATAFRAME
# ========================================================

df = pd.DataFrame(libri)


# ========================================================
# CORREZIONE FINALE DELL'ENCODING
# ========================================================

colonne_testo = [
    "titolo",
    "autore",
    "categoria",
    "editore_anno"
]

for colonna in colonne_testo:

    if colonna in df.columns:

        df[colonna] = df[colonna].apply(
            correggi_encoding
        )


# ========================================================
# CONTROLLO DUPLICATI
# ========================================================

df = df.drop_duplicates(
    subset=["posizione"],
    keep="first"
)

df = df.sort_values(
    "posizione"
).reset_index(drop=True)


# ========================================================
# CONTROLLO FINALE
# ========================================================

print("\n")
print("=" * 60)
print("CONTROLLO FINALE")
print("=" * 60)

print(
    "Numero libri:",
    len(df)
)

if not df.empty:

    print(
        "Prima posizione:",
        df["posizione"].min()
    )

    print(
        "Ultima posizione:",
        df["posizione"].max()
    )


if len(df) == 100:

    print(
        "\n✅ Abbiamo raccolto esattamente 100 libri."
    )

else:

    print(
        "\n⚠️ ATTENZIONE: il numero di libri non è 100."
    )


# ========================================================
# CONTROLLO POSIZIONI
# ========================================================

posizioni_attese = set(range(1, 101))

posizioni_trovate = set(
    df["posizione"]
)

mancanti = sorted(
    posizioni_attese - posizioni_trovate
)

if not mancanti:

    print(
        "✅ Tutte le posizioni da 1 a 100 sono presenti."
    )

else:

    print(
        "⚠️ Posizioni mancanti:",
        mancanti
    )


# ========================================================
# CONTROLLO VALORI MANCANTI
# ========================================================

print("\nValori mancanti per colonna:\n")

print(
    df.isna().sum()
)


# ========================================================
# CONTROLLO ENCODING
# ========================================================

print("\nControllo encoding:\n")

for colonna in colonne_testo:

    if colonna not in df.columns:
        continue

    valori = df[colonna].dropna().astype(str)

    numero_sospetti = valori.apply(
        lambda x: any(
            c in x
            for c in ("Ã", "Â", "â", "ð")
        )
    ).sum()

    if numero_sospetti == 0:

        print(
            f"✅ {colonna}: nessun carattere sospetto"
        )

    else:

        print(
            f"⚠️ {colonna}: "
            f"{numero_sospetti} valori sospetti"
        )


# ========================================================
# PRIME 10 RIGHE
# ========================================================

print("\nPrime 10 righe:\n")

print(
    df.head(10).to_string(
        index=False
    )
)


# ========================================================
# SALVATAGGIO CSV
# ========================================================

nome_file = "classifica_ibs_fase1.csv"

df.to_csv(
    nome_file,
    index=False,
    encoding="utf-8-sig"
)

print(
    f"\n✅ File salvato come: {nome_file}"
)
