# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 09:48:16 2021

@author: Domenico
"""

import requests
import argparse
import json
import re
#import pandas as pd
    
parser = argparse.ArgumentParser()
parser.add_argument("-o1", "--out_data1", help="Complete path il file input_data.json", 
                     type=str, default='./FileProva1.json')
parser.add_argument("-o2", "--out_data2", help="Complete path il file input_data.json", 
                     type=str, default='./Lista_HyperLinks.json')
args = parser.parse_args()

#Url d'Analisi http://www.sialserramentisrl.it
Url= requests.get('http://www.sialserramentisrl.it')
#Quando lanciate una richiesta, Requests fa delle ipotesi sull’encoding della risposta
#sulla base degli header HTTP. L’encoding del testo utilizzato da Requests si applica al contenuto di Url.text.
#Potete scoprire quale encoding viene usato da Requests e cambiarlo usando la property Url.encoding
Status_Url=Url.status_code
if  Status_Url == 200:
    Html=Url.text
    Info_Url=Url.headers
    Links = re.findall('''<a\s+(?:[^>]*?\s+)?href="([^"]*)"''', str(Html))
    #Info=pd.DataFrame(Info_Url)
    print(Info_Url)
else:
    print('Error 404 NOT FOUND')
    
with open(args.out_data1, 'w') as f:
    json.dump(Html, f)

with open(args.out_data2, 'w') as f:
    json.dump(Links, f, indent=3)