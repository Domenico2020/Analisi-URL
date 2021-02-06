#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 13:20:09 2021

@author: Egidio e Domenico
"""

from abc import ABC, abstractmethod
import re
from os.path import splitext
import pandas as pd 
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
    def create_instance(filename, colonna):
        suffix = splitext(filename)[1][1:].lower()
        if suffix == 'txt':
            return TXTReader(filename)
        elif suffix == 'xlsx':
            return XLSXReader(filename, colonna)
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
        list_of_urls_temp = fin.readlines()
        list_of_urls = []
        for url in list_of_urls_temp:
            url = re.findall(r'(https?://[^\s]+)', url)[0]
            list_of_urls.append(url)
        return list_of_urls
    
"""
La sottoclasse XLSXReader legge un file .xlsx, contenente una lista di url, e 
restituisce una lista python contenente quella lista di url
"""
    
class XLSXReader(UrlReader):

    def __init__(self, filename, colonna):
        self.filename = filename
        self.colonna = colonna

    def get_list_of_url(self):
        fin = pd.ExcelFile(self.filename) 
        sheetX = fin.parse(0)
        list_of_urls = sheetX[self.colonna].tolist()
        return list_of_urls