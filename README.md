# Analisi-URL:
Analisi della Profondità delle pagine Web

L'analisi ha inizio con una pagina web (http://www.sialserramentisrl.it) contenente pochi link al suo interno così da facilitarci nella costruzione dell'algoritmo. 
Utilizziamo la libreria "requests" che ci permette di ottenere, non solo informazioni sullo stato della pagina web, ma anche la struttura completa della pagina web stessa (.file.html).
Inolre la libreria "re" (regular expression), tramite la funzione findall(), ci permette di ottenere tutte le corrispondenze relative agli hyperlink nel testo. Questi hyperlink presenti nel testo li salviamo in Links come una lista di stringhe.
Lo stato della pagina ci permette di verificare la disponibilità o meno di quest'ultima rilasciando un valore pari a "200" se la pagina Web è on-line. Al contrario se la pagina web è off-line, viene stampato "Error 404 NOT FOUND".
Il programma restituisce quindi in formato .json sia la pagina html che la lista degli hyperlink presenti nella pagina.
