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
from cleaner import ListCleaner

"""
Si utilizza il parser per la lettura dei file in input e per la scrittura dei file in output
"""
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--in_data", help="Scrivere il path completo per il file di input", 
                    default='./data/lista.txt')
parser.add_argument("-o", "--out_data", help="Scrivere il path completo per il file di output", 
                    default='./Lista_HyperLinks.json')
parser.add_argument("-md", "--max_depth", help="Scrivere la profondità massima a cui arrivare", 
                    type=int, default=2)
args = parser.parse_args()



"""
MAIN
"""

# Si acquisisce la lista degli url 
reader = UrlReader.create_instance(args.in_data)
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
    extractor.get_links_iteratively(url, "", set([url]), args.max_depth)
list_of_links = extractor.list_of_links
list_of_cycles = extractor.list_of_cycles

# Si eliminano dalla lista dei link i valori non voluti
cleaner = ListCleaner()
list_of_links = cleaner.drop_duplicates(list_of_links)
list_of_links = cleaner.drop_none_values(list_of_links)

data = {
    "Le liste in uscita sono": {
        "Lista di link": list_of_links ,
        "Lista di cicli": list_of_cycles
    }
}

# Si salva la lista di hyperlink in un file json
with open(args.out_data, 'w') as f:
    json.dump(data, f, indent=3)