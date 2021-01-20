# Analisi-URL:
Analisi della Profondità delle pagine Web

L'analisi ha inizio con l'acquisizione di un tre url e la loro successiva memorizzazione in una lista. 
Viene analizzato un url alla volta mediante un ciclo for.
Utilizziamo la libreria "requests" che ci permette di ottenere informazioni sullo stato della pagina web.
Lo stato della pagina ci permette di verificare la disponibilità o meno di quest'ultima rilasciando un valore pari a "200" se la pagina Web è on-line. 
Tramite un algorirmo di visita in profondità visitiamo tutti i link, fino ad un livello scelto di profondità (2, in questo caso).
I link visitati vengono salvati in una lista, e cosi quindi per ogni url acquisito inizialmente.
Il programma restituisce quindi in formato .json la lista degli hyperlink presenti nella pagina.
