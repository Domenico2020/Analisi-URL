#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 22:19:22 2021

@authors: Egidio e Domenico
"""

import argparse
from abc import ABC, abstractmethod
import re
from os.path import splitext
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd 

"""
Si utilizza il parser per la lettura dei file in input e per la scrittura dei file in output
"""
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--in_data", help="Scrivere il path completo per il file di input", 
                      type=str, default='./inputdata/lista.txt')
parser.add_argument("-o", "--out_data", help="Scrivere il path completo per il file di output", 
                     type=str, default='./outputdata/Lista_HyperLinks.json')
parser.add_argument("-o1", "--out_dataError", help="Scrivere il path completo per il file di output degli errori", 
                     type=str, default='./outputdata/Lista_HyperLinksError.json')
parser.add_argument("-P", "--paramers", help="Parametro di profondità depth", 
                     type=int, default=2)
args = parser.parse_args()
#Inizzializzazione variabile per il Crowler
list_of_links=[]
"""
Si crea la classe astratta che rimanda tramite il metodo statico alle classi TXTReader
ed XLSXReader. Questa classe contiene il metodo astratto get_list_of_url() che segue 
una differente implementazione in base al suffiso del file in input.
"""

class UrlReader(ABC):
    """
    interface
    """

    @abstractmethod
    def get_list_of_url(self):
        """
        abstract method
        """
        pass

    @staticmethod
    def create_instance(filename):
        suffix = splitext(filename)[1][1:].lower()
        if suffix == 'txt':
            return TXTReader(filename)
        elif suffix == 'xlsx':
            return XLSXReader(filename)
        else:
            raise ValueError('unknown file type')

"""
La sottoclasse TXTReader legge un file .txt, contenente una lista di url, e 
restituisce una lista python contenente quella lista di url
"""

class TXTReader(UrlReader):

    def __init__(self, filename):
        self.filename = filename

    def get_list_of_url(self):
        fin = open(self.filename, 'r') 
        list_of_urls = fin.readlines()
 
        return list_of_urls
    
"""
La sottoclasse XLSXReader legge un file .xlsx, contenente una lista di url, e 
restituisce una lista python contenente quella lista di url
"""
    
class XLSXReader(UrlReader):

    def __init__(self, filename):
        self.filename = filename

    def get_list_of_url(self):
        fin = pd.ExcelFile(self.filename) 
        sheetX = fin.parse(0)
        list_of_urls = sheetX['URL'].tolist()
        return list_of_urls
"""
La sottoclasse DFSCrawler riceve in input la lista degli url che tramite il metodo 
della classe get_links() ne estra uno alla volta. Quindi il metodo get_links() richiama
il secondo metodo della classe get_links_iteratively() che a sua volta tramite una visita in 
profondità analizza l'url e tutte le pagine che questo riferisce restituendo la lista degli
hyperlink (list_of_links) collegati all'url analizzato
"""
class DFSCrawler():
    
    def __init__(self):
        pass
    
    def get_links(self, list_of_urls):
        for url in list_of_urls:
            url = re.findall(r'(https?://[^\s]+)', url)[0]
            print(' ')
            print(' ')
            print(url)
            list_of_links = self.get_links_iteratively(url, "", set([url]), max_depth=args.paramers)
            list_of_links.append("i precenti link fanno riferimento a:"+ (url))
        return list_of_links
    
    def get_links_iteratively(self, base, path, visited, max_depth=args.paramers, depth=0):
        list_e = []
        
        if depth < max_depth:
            try:
                soup = BeautifulSoup(requests.get(base + path).text, "html.parser")
                for link in soup.find_all("a"):
                    href = link.get("href")
                    if href not in visited:
                        visited.add(href)
                        list_of_links.append(href)
                        list_of_links.append(f"at depth {depth}: {href}")
                        print(f"at depth {depth}: {href}")
                        if href.startswith("http"):
                            self.get_links_iteratively(href, "", visited, max_depth, depth + 1)
                        else:
                            self.get_links_iteratively(base, href, visited, max_depth, depth + 1)
                    else:                       
                        list_e.append(href)
            except:
                pass
            
        return list_of_links

"""
La sottoclasse ListCleaner riceve la lista dei link e rimuove i '#', cancella le pagine che si
ripetono ed elimina i valori 'None'
"""
class ListCleaner():
    
    def __init__(self):
        pass
    
    def clean_list(self, list_of_links):
        try:
         list_of_links.remove("#")
        except:
          pass
         
        return list_of_links
    
    def drop_duplicates(self, list_of_links):
        try:
          list_of_links = list(dict.fromkeys(list_of_links))
        except:
            pass
        return list_of_links
    
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
list_of_links = extractor.get_links(list_of_urls)
list_of_links = list(list_of_links)
# Si eliminano dalla lista dei link i valori non voluti
cleaner = ListCleaner()


list_e = extractor.get_links(list_of_urls)

list_of_links = cleaner.clean_list(list_of_links)
list_of_links = cleaner.drop_duplicates(list_of_links)
list_of_links = cleaner.drop_none_values(list_of_links)



with open(args.out_data, 'w') as f:
    json.dump(list_of_links, f, indent=3)

with open(args.out_dataError, 'w') as k:
    json.dump(list_e, k, indent=3)
    
    
    
    
    
    
    
    
    
    



