#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  2 00:59:44 2021

@author: Egidio
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
"""
La classe DFSCrawler riceve in input un url che tramite una visita in profondità 
analizza l'url e tutte le pagine che questo riferisce definendo la lista degli
hyperlink (list_of_links) e la lista dei cicli (list_of_cycles) collegati all'url  
ricevuto come input
"""
class DFSCrawler():
     
    def __init__(self):
        self.list_of_links = []
        self.list_of_cycles = []
        self.list_of_error = []
    
    # il crawler
    def get_links_recursively(self, base, path, visited, max_depth):
        if 0 < max_depth:
            try:
                soup = BeautifulSoup(requests.get(base + path).text, "html.parser")
                for link in soup.find_all("a"):
                    href = link.get("href")
                    if href not in visited:
                        visited.add(href)                      
                        if href is not None:
                            # Non si considerano i link alla mail
                            if href.startswith('mailto:'):
                                pass
                            # Non si considerano i link al telefono
                            elif href.startswith('tel'):
                                pass
                            else: 
                                if not href.startswith('http'):
                                    joint = urljoin(base, href)
                                    self.list_of_links.append(joint)                               
                                if not href.startswith('https'):
                                    joint = urljoin(base, href)
                                    self.list_of_links.append(joint)
                                if href.startswith('http'):
                                    self.list_of_links.append(href)
                                if href.startswith('https'):
                                    self.list_of_links.append(href)
                        print(f"at depth {max_depth}: {href}")
                        if href.startswith("http"):                   
                            self.get_links_recursively(href, "", visited, max_depth-1)
                        else:
                            self.get_links_recursively(base, href, visited, max_depth-1)
                    else:
                        self.list_of_cycles.append(href)
            except:
                pass
                

