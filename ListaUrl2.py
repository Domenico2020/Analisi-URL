#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 22:19:22 2021

@authors: Egidio e Domenico
"""

import argparse
from abc import ABC, abstractmethod
from os.path import splitext
import re
import requests
from bs4 import BeautifulSoup
import json

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--in_data", help="Complete path il file input_data.json", 
                     type=str, default='./lista.txt')
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
    
class DFSCrawler:
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_links_iteratively(base, path, visited, max_depth=2, depth=0):
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
                            links.get_links_iteratively(href, "", visited, max_depth, depth + 1)
                        else:
                            links.get_links_iteratively(base, href, visited, max_depth, depth + 1)
            except:
                pass
            
        return list_of_links

    
        
# acquisisci lista di url e memorizzala in una lista
list_of_urls = []

reader = UrlReader.create_instance(args.in_data)
stringa = reader.get_list_of_url()

list_of_urls = re.findall(r'(https?://[^\s]+)', stringa)

list_of_links = []
for url in list_of_urls:
    # Si analizza l'url... fetch (preleva)
    url_rqst = requests.get(url)
    # Si verifica la disponibilità della pagina
    status_url = url_rqst.status_code
    if  status_url == 200:
        html = url_rqst.text
        print(' ')
        print(' ')
        print(url)
        links = DFSCrawler()
        list_of_links = links.get_links_iteratively(url, "", set([url]), max_depth=2, depth=0)


with open(args.out_data, 'w') as f:
    json.dump(list_of_links, f, indent=3)



