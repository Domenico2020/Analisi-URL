Data una lista di url in input come file .txt o .xlsx il programma restituisce come lista tutte le pagine raggiungibili da quell'url in modo ricorsivo fino ad una certa profondità e le salva in output come file .json. Se una pagina riferisce più volte ad una stessa pagina quest'ultima viene inculsa una sola volta nella lista delle pagine restituite. Inoltre il programma riconosce la presenza di cicli nella catena di pagine esplorate, a partire da un dato url.

Per accedere alle pagine web e trovare in esse gli hyperlink sono usati i moduli "requests" e "BeautifulSoup".
