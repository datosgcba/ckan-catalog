#from data_lib.migraciones import ListarRecursos
from ckanapi import RemoteCKAN
import requests
from datetime import date, datetime
import csv

import json
import os,sys,inspect

# Import organizaciones from common
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
data_lib_dir = os.path.join(parent_dir, "data_lib/")
sys.path.insert(0,data_lib_dir) 
import migraciones as util_migraciones
import recursos as util_recursos
import datasets as util_datasets
import organizaciones as util_org

# Setea variables de configuración

if ('url_origen' in os.environ):
    url_origen=os.environ['url_origen']
else:
    exit('No existe url_origen')

if ('apikey_origen' in os.environ):
    apikey_origen=os.environ['apikey_origen']
else:
    exit('No existe apikey_origen')

"""url_origen = settings.url_origen #url del portal de origen
apikey_origen = settings.apikey_origen    #apikey del usuario de portal de origen
url_destino = settings.url_destino #url del portal de origen
apikey_destino = settings.apikey_destino    #apikey del usuario de portal de origen"""

ua_origen = 'ckanapiexample/1.0'+url_origen
portal_origen = RemoteCKAN(url_origen, apikey_origen, user_agent=ua_origen)

#ua_destino = 'ckanapiexample/1.0'+url_destino
#portal_destino = RemoteCKAN(url_destino, apikey_destino, user_agent=ua_destino)

def CatalogoDataset():
    listaDatasets = []
    datasetList = util_datasets.GetDatasetsList(portal_origen)

    for dataset in datasetList:
        datasetPackage=util_datasets.DetallarPackageDataset(portal_origen, dataset)
        organization=datasetPackage['organization'].get('title')


        for e in datasetPackage['extras']:
                if e['key'] == "updateFrequency":
                    continue
        
        listaDatasets.append([str(organization),
                                str(datasetPackage['name']),
                                str(datasetPackage['title']),
                                str('https://data.buenosaires.gob.ar/dataset/'+datasetPackage['name']),
                                str(e['value']),
                                str(datasetPackage['metadata_modified'])])
        #print(datasetPackage['name'])

    # Genera catalogo de datasets
    catalogo = f"'organizacion';'dataset id';'nombre dataset';'url';'frecuencia actualizacion';'ultima modificacion'\n"
    for data in listaDatasets:
        
        for d in data:
            catalogo = catalogo + (d+';')

        catalogo = catalogo + ('\n')
    print(catalogo)
    
    return listaDatasets
