#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 23:37:49 2021

@author: Egidio
"""

"""
La sottoclasse ListCleaner riceve la lista dei link, cancella le pagine che si
ripetono ed elimina i valori 'None'
"""
class ListCleaner():
    
    def __init__(self):
        pass
    
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

    