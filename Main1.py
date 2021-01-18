# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 09:48:16 2021

@author: Domenico ed Egidio
"""

"""
Si scrive un algoritmo che dato un url in ingresso restituisce la lista degli
hyperlink presenti nell'url'.
"""

import argparse
from abc import ABC, abstractmethod
from os.path import splitext
import os
import json
import re
import requests

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--in_data", help="Complete path il file input_data.json", 
                     type=str, default='./lista2.txt')
parser.add_argument("-o", "--out_data", help="Complete path il file input_data.json", 
                     type=str, default='./Lista_HyperLinks.json')
args = parser.parse_args()

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
        else:
            raise ValueError('unknown file type')
        

class TXTReader(UrlReader):

    def __init__(self, filename):
        self.filename = filename

    def get_list_of_url(self):
        fin = open(self.filename, 'r')
        text = fin.read()
        return text
            
# acquisisci lista di url e memorizzala in una lista
list_url = []
reader = UrlReader.create_instance(args.in_data)
stringa = reader.get_list_of_url()
list_url = re.findall(r'(https?://[^\s]+)', stringa)

print('Questi sono gli Url:')
print(list_url)
print('Inserisci il nome del sito da Analizzare:')
a = str(input())
print(' ')
print('Il sito inserito è: ' +a)
print(' ')
# Si analizza l'url
url_rqst = requests.get(a)
# Si verifica la disponibilità della pagina
status_url = url_rqst.status_code
if  status_url == 200:
    html = url_rqst.text
    new_links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', str(html))
else:
    # stampa le pagine non disponibili
    print('--------- off-line'+str(a)) 

a = a.replace("http://", "_")
a = a.replace("https://", "_")
estx = os.path.splitext(args.out_data)[1]   
args.out_data = os.path.splitext(args.out_data)[0]+a+'_'+estx
with open(args.out_data, 'w') as f:
    json.dump(new_links, f, indent=3)