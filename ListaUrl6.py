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
#immpota la lista di inpunt e i due file di out più il parametro 
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--in_data", help="Complete path il file lista.txt", 
                     type=str, default='./data/lista2.txt')
parser.add_argument("-o", "--out_data", help="Complete path il file Lista_HyperLinks.json", 
                     type=str, default='./Lista_HyperLinks.json')
parser.add_argument("-o1", "--out_dataError", help="Complete path il file Lista_HyperLinksError.json", 
                     type=str, default='./Lista_HyperLinksError.json')
parser.add_argument("-P", "--paramers", help="Parametro di profondità depth", 
                     type=int, default=2)
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
            
    # def create_instanceExlsx(filename):
    #     suffix = splitext(filename)[1][1:].lower()
    #     if suffix == 'xlsx':
    #         return ExlsxReader(filename)
    #     else:
    #         raise ValueError('unknown file type')
        

class TXTReader(UrlReader):

    def __init__(self, filename):
        self.filename = filename

    def get_list_of_url(self):
        fin = open(self.filename, 'r') 
        list_of_urls = fin.readlines()
        return list_of_urls
        
# class  ExlsxReader(UrlReader):

#     def __init__(self, filename):
#         self.filename = filename

#     def get_list_of_url1(self):
#         fin = open(self.filename, 'r') 
#         list_of_urls = fin.readlines()        
#         return list_of_urls
    
class DFSCrawler():
    
    def __init__(self):
        pass
    
    def get_links(self, list_of_urls):
        
        for url in list_of_urls:
            # Si analizza l'url... fetch (preleva)
            url = re.findall(r'(https?://[^\s]+)', url)
            url = url[0]
            url_rqst = requests.get(url)
            # Si verifica la disponibilità della pagina
            status_url = url_rqst.status_code
            if  status_url == 200:
                #html = url_rqst.text
                print(' ')
                print(' ')
                print(url)
                list_of_links = self.get_links_iteratively(url, "", set([url]), max_depth=args.paramers)
        #     else:
        #         print('')
        return list_of_links
    
    def get_links_iteratively(self, base, path, visited, max_depth=args.paramers, depth=0):
        list_e=[]
        if depth < max_depth:
            try:
                soup = BeautifulSoup(requests.get(base + path).text, "html.parser")
                for link in soup.find_all("a"):
                    href = link.get("href")
                    if href not in visited:
                        visited.add(href)
                        list_of_links.append(href)
                        print(f"at depth {depth}: {href}")
                        if href.startswith("http"):
                            self.get_links_iteratively(href, "", visited, max_depth, depth + 1)
                        else:
                            self.get_links_iteratively(base, href, visited, max_depth, depth + 1)
                    #else:
                        #print('')
            except:
                print('Error')
                list_e.append(base)
                pass
        
        return list_of_links

    
        
# main
reader = UrlReader.create_instance(args.in_data)
# reader = UrlReader.create_instanceExlsx(args.in_data)
list_of_urls = reader.get_list_of_url()

list_of_links = []
extractor = DFSCrawler()
list_of_links = extractor.get_links(list_of_urls)



#list_e = extractor.get_links(list_of_urls)
#list_of_links = list(set(list_of_links))
#Lista degli errori non funzionante
#list_e1 = list(set(list_e)-set(list_of_links))

with open(args.out_data, 'w') as f:
    json.dump(list_of_links, f, indent=3)
    
# with open(args.out_dataError, 'w') as k:
#     json.dump(list_e, k, indent=3)



