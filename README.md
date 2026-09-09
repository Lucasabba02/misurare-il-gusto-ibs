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

## Stato del progetto

Fase 1 completata: raccolta e controllo dei 100 libri della classifica IBS. Con la prima fase del progetto e il primo codice generato, dal sito web di IBS, e nello specifico dalla pagina dedicata alla classifica settimanale dei libri venduti, abbiamo estratto POSIZIONE, TITOLO, AUTORE, URL, RATING, NUMERO DI RECENSIONI, CATEGORIA, EDITORE e ANNO dei libri presenti nella top 100. Bisogna considerare per correttezza che nella top 100 dei libri venduti appaiono anche i preordini di libri non ancora usciti, che quindi non avranno né recensioni né rating. 
Dopo aver estratto la top 100 in un file CSV mi sono reso conto che c'erano degli elementi di troppo che non sarebbero stati utili nell'analisi o degli errori di copiatura di alcuni caratteri ricorrenti, come "è", "à". Tra gli elementi inutili c'erano per esempio dei link che rimandavano ad altre sezioni del sito web o che consigliavano libri simili. Ho provveduto alla rimozione, tramite richiesta di ulteriori strisce di codice al LLM, lasciando nel CSV finale solo gli elementi di classificazione che più mi interessavano. Per i caratteri trascritti erroneamente, ho dato indicazione al LLM di creare un codice per il quale, qualora fossero stati rilevati quei caratteri, venissero ritrascritti così com'erano. 
Una volta generato il file CSV della top 100 ho controllato a campione i titoli presenti, che effettivamente combaciavano con quanto indicato sul sito. Il codice dava un errore solo per un libro che non presentava il nome di un autore, dal momento che era una raccolta di testi "a cura di...". 
Avendo svolto questo lavoro di scraping a cavallo tra due settimane, la classifica di IBS si è nel frattempo aggiornata e, riavviando il codice, ho potuto constatare che estraeva dal sito la nuova classifica top 100; anche se (devo ammetterlo), più per casualità che per altro, questo mi ha confermato che il codice può funzionare nel tempo e non è legato a una settimana precisa. 

Fase 2
