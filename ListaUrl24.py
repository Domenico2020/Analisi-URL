#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 22:19:22 2021

@authors: Egidio e Domenico
"""

import argparse
import json
from reader import UrlReader
from crawler import DFSCrawler

"""
Si utilizza il parser per la lettura dei file in input e per la scrittura dei file in output
"""
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--in_data", help="Scrivere il path completo per il file di input", 
                    default='./data/lista_semplice.txt')
parser.add_argument("-o", "--out_data", help="Scrivere il path completo per il file di output", 
                    default='./Lista_HyperLinks.json')
parser.add_argument("-d", "--max_depth", help="Scrivere la profondità massima a cui arrivare", 
                    type=int, default=2)
parser.add_argument("-u", "--colonna_Url", help="Scrivere la colonna contenente gli Url", 
                    type=str, default='URL')
args = parser.parse_args()



"""
MAIN
"""

# Si acquisisce la lista degli url 
reader = UrlReader.create_instance(args.in_data, args.colonna_Url)
list_of_urls = reader.get_list_of_url()

# Si estraggono gli hyperlink presenti in ogni url e li si salva in una lista
extractor = DFSCrawler()
for url in list_of_urls:
    print(' ')
    print(' ')
    print(url)  
    extractor.list_of_links.append(
                    "-------------- I LINK SEGUENTI FANNO RIFERIMENTO A: "
                    + url + " --------------")
    extractor.list_of_cycles.append(
                    "-------------- I LINK SEGUENTI FANNO RIFERIMENTO A: "
                    + url + " --------------")
    extractor.list_of_errors.append(
                    "-------------- I LINK SEGUENTI FANNO RIFERIMENTO A: "
                    + url + " --------------")
    extractor.get_links_recursively(url, "", set([url]), args.max_depth)
list_of_links = extractor.list_of_links
list_of_cycles = extractor.list_of_cycles
list_of_errors = extractor.list_of_errors
data = {
    "Le liste in uscita sono nel formato: 'pagina figlia: pagina padre' ": {
        "Lista di link": list_of_links ,
        "Lista di cicli": list_of_cycles,
        "Lista degli errori": list_of_errors
    }
}

# Si salva la lista di hyperlink in un file json
with open(args.out_data, 'w') as f:
    json.dump(data, f, indent=3)