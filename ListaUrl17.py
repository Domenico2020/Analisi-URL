#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 22:19:22 2021

@authors: Egidio e Domenico
"""

import argparse
import requests
from bs4 import BeautifulSoup
import json
from reader import UrlReader

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
La sottoclasse DFSCrawler riceve in input la lista degli url che tramite il metodo 
della classe get_links() ne estrae uno alla volta. Quindi il metodo get_links() richiama
il secondo metodo della classe get_links_iteratively() che a sua volta tramite una visita in 
profondità analizza l'url e tutte le pagine che questo riferisce restituendo la lista degli
hyperlink (list_of_links) collegati all'url analizzato
"""
class DFSCrawler():
    
   
    def __init__(self):
        pass
    
    
    # il crawler
    def get_links_iteratively(self, base, path, visited, max_depth):
        if 0 < max_depth:
            try:
                list_of_links.append("i link fanno riferimento a: "+ url)
                soup = BeautifulSoup(requests.get(base + path).text, "html.parser")
                for link in soup.find_all("a"):
                    href = link.get("href")
                    if href not in visited:
                        visited.add(href)
                        list_of_links.append(href)
                        print(f"at depth {max_depth}: {href}")
                        if href.startswith("http"):                   
                            self.get_links_iteratively(href, "", visited, max_depth-1)
                        else:
                            self.get_links_iteratively(base, href, visited, max_depth-1)
            except:
                pass
                # Qui bisongna gestire il riferimento circolare (list_of_cycles)
        return list_of_links

"""
La sottoclasse ListCleaner riceve la lista dei link e rimuove i '#', cancella le pagine che si
ripetono ed elimina i valori 'None'
"""
class ListCleaner():
    
    def __init__(self):
        pass
    
    # Si rimuovono i '#'
    def clean_list(self, list_of_links):
        list_of_links.remove("#")
        return list_of_links
    
    # Si cancellano le pagine che si ripetono
    def drop_duplicates(self, list_of_links):
        list_of_links = list(dict.fromkeys(list_of_links)) # Si converte la lista 'list_of_links'
        return list_of_links                               # in un dizionario, per cancellare le 
                                                           # pagine che si ripetono, quindi si 
                                                           # estraggono le chiavi che vengono 
                                                           # convertite in una lista che viene
    # Si eliminanoi i valori  'None'                       # salvata in 'list_of_links'
    def drop_none_values(self, list_of_links):
        list_of_links = list(filter(None.__ne__, list_of_links))
        return list_of_links
        
    
"""
MAIN
"""

# Si acquisisce la lista degli url 
reader = UrlReader.create_instance(args.in_data)
list_of_urls = reader.get_list_of_url()

# Si estraggono gli hyperlink presenti in ogni url e li si salva in una lista
extractor = DFSCrawler()
list_of_links = []

for url in list_of_urls:
    print(' ')
    print(' ')
    print(url)
    extractor.get_links_iteratively(url, "", set([url]), args.max_depth)

# Si eliminano dalla lista dei link i valori non voluti
cleaner = ListCleaner()
list_of_links = cleaner.clean_list(list_of_links)
list_of_links = cleaner.drop_duplicates(list_of_links)
list_of_links = cleaner.drop_none_values(list_of_links)

# Si salva la lista di hyperlink in un file json
with open(args.out_data, 'w') as f:
    json.dump(list_of_links, f, indent=3)

    
    
    
    
    
    
    
    
    
    
    
    



