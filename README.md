# Misurare il gusto: descrizioni promozionali e visibilità commerciale dei libri

## Domanda di ricerca

Quali caratteristiche della descrizione promozionale dei libri sono associate alle diverse fasce di visibilità commerciale nelle classifiche IBS?

## Obiettivo

Analizzare le caratteristiche linguistiche e promozionali presenti nelle descrizioni dei libri e verificare se alcune di esse risultano associate alle fasce più alte o più basse della classifica commerciale IBS.

## Dati

Il progetto utilizza i 100 libri presenti nella classifica generale IBS dei libri più venduti nell'ultima settimana, rilevata in una specifica data.

## Metodologia

Il progetto prevede:

1. raccolta automatica dei dati dalla classifica IBS;
2. raccolta delle descrizioni delle singole schede libro;
3. classificazione sistematica delle caratteristiche linguistiche delle descrizioni mediante un LLM;
4. controllo umano su un campione;
5. analisi quantitativa tramite Python;
6. interpretazione critica dei risultati.

### Motivazione della scelta del metodo di acquisizione
Per la raccolta dei dati è stato utilizzato il **web scraping delle pagine HTML pubblicamente accessibili di IBS.it**, anziché il ricorso alle API. La scelta è dovuta principalmente al fatto che le API disponibili di IBS non forniscono un'interfaccia pubblica e documentata specificamente orientata all'accesso ai dati necessari per questo progetto, in particolare alla **classifica dei libri e alle relative descrizioni promozionali**. Lo scraping dell'HTML ha quindi permesso di raccogliere direttamente le informazioni effettivamente visualizzate agli utenti sul sito, mantenendo coerenza tra i dati utilizzati nell'analisi e il contenuto pubblico della piattaforma.

## Stato del progetto

## Fase 1 completata: raccolta e controllo dei 100 libri della classifica IBS. 

Con la prima fase del progetto e il primo codice generato, dal sito web di IBS, e nello specifico dalla pagina dedicata alla classifica settimanale dei libri venduti, abbiamo estratto POSIZIONE, TITOLO, AUTORE, URL, RATING, NUMERO DI RECENSIONI, CATEGORIA, EDITORE e ANNO dei libri presenti nella top 100. Bisogna considerare per correttezza che nella top 100 dei libri venduti appaiono anche i preordini di libri non ancora usciti, che quindi non avranno né recensioni né rating. 
Dopo aver estratto la top 100 in un file CSV mi sono reso conto che c'erano degli elementi di troppo che non sarebbero stati utili nell'analisi o degli errori di copiatura di alcuni caratteri ricorrenti, come "è", "à". Tra gli elementi inutili c'erano per esempio dei link che rimandavano ad altre sezioni del sito web o che consigliavano libri simili. Ho provveduto alla rimozione, tramite richiesta di ulteriori strisce di codice al LLM, lasciando nel CSV finale solo gli elementi di classificazione che più mi interessavano. Per i caratteri trascritti erroneamente, ho dato indicazione al LLM di creare un codice per il quale, qualora fossero stati rilevati quei caratteri, venissero ritrascritti così com'erano. 
Una volta generato il file CSV della top 100 ho controllato a campione i titoli presenti, che effettivamente combaciavano con quanto indicato sul sito. Il codice dava un errore solo per un libro che non presentava il nome di un autore, dal momento che era una raccolta di testi "a cura di...". 
Avendo svolto questo lavoro di scraping a cavallo tra due settimane, la classifica di IBS si è nel frattempo aggiornata e, riavviando il codice, ho potuto constatare che estraeva dal sito la nuova classifica top 100; anche se (devo ammetterlo), più per casualità che per altro, questo mi ha confermato che il codice può funzionare nel tempo e non è legato a una settimana precisa. 

## Fase 2 – Raccolta delle descrizioni

A partire dal dataset ottenuto nella Fase 1, è stata effettuata la raccolta delle descrizioni promozionali dei 100 libri presenti nella classifica settimanale IBS. Per ogni libro è stata utilizzata la URL presente nel dataset della Fase 1 e, tramite uno script Python basato su `requests` e `BeautifulSoup`, è stata visitata la relativa pagina IBS. È stata estratta l'intera sezione HTML `#pdp-descrizione`, comprendendo quindi non solo la sinossi del libro, ma anche eventuali citazioni di recensioni, premi, riconoscimenti, giudizi promozionali e altre informazioni presenti nella sezione "Descrizione", come anche gli argomenti del libro.
Il risultato della raccolta è il file: `classifica_ibs_fase2 07.09.csv`

Il dataset contiene le seguenti informazioni:

- posizione nella classifica
- titolo
- autore
- URL della pagina IBS
- descrizione completa

## Pulizia del file
Controllando che il file CSV fosse pulito ho notato che nella descrizione compariva sempre "Leggi di più leggi di meno". Su Colab ho quindi inserito uno script per eliminare queste scritte che avrebbero creato rumore nell'analisi delle descrizioni. 
Ho notato inoltre che il libro n°87 non contiene una descrizione. Si tratta di un libro scolastico. Ignoreremo la cosa. 
Inoltre, nelle descrizioni dei libri veniva sempre copiata all'inizio la parola "Descrizione", che evidentemente faceva parte dell'interfaccia di IBS. Con il secondo script di pulizia, ho eliminato questa parola. 



