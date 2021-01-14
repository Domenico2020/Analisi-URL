# Analisi-URL
 Analisi della Profondità delle pagine Web

L'analisi ha inizio con una pagina web (http://www.sialserramentisrl.it) contenente pochi link interni così da facilitarci la costruzione dell'algoritmo. 
Utilizziamo la libreria "requests" che ci permette di ottenere non solo informazioni sullo stato della pagina ma anche la struttura completa della pagina web (.file.html).
Lo stato della pagina ci permette di verificare la disponibilità o meno di quest'ultima rilasciando un valore pari a "200" se la pagina Web è on-line, se è off-line 
viene stampato "Error 404 NOT FOUND".
