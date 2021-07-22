#from data_lib.migraciones import ListarRecursos
from ckanapi import RemoteCKAN
import requests
from datetime import date, datetime
import settings
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

url_origen = settings.url_origen #url del portal de origen
apikey_origen = settings.apikey_origen    #apikey del usuario de portal de origen
url_destino = settings.url_destino #url del portal de origen
apikey_destino = settings.apikey_destino    #apikey del usuario de portal de origen

ua_origen = 'ckanapiexample/1.0'+url_origen
portal_origen = RemoteCKAN(url_origen, apikey_origen, user_agent=ua_origen)
ua_destino = 'ckanapiexample/1.0'+url_destino
portal_destino = RemoteCKAN(url_destino, apikey_destino, user_agent=ua_destino)

listaRecursos = []
orgs = util_org.GetListaOrganizaciones(portal_destino)

for organizacion in orgs:
    datasets=util_datasets.GetDatasetsOrganizacion(portal_destino, organizacion)

    for dataset in datasets:
        datasetExtra=util_datasets.DetallarPackageDataset(portal_destino, dataset['name'])
        recursos=util_recursos.DetallarRecurso(portal_destino, dataset['name'])
        
        for e in datasetExtra['extras']:
            if e['key'] == "updateFrequency":
                continue
            
        for r in recursos:
            last_modified = str(r['last_modified']) if str(r['last_modified']) != 'None' else str(r['created'])
            
            listaRecursos.append([str(organizacion),
                                    str(dataset['name']),
                                    str(dataset['title']),
                                    str('https://data.buenosaires.gob.ar/dataset/'+dataset['name']),
                                    str(e['value']),
                                    str(r['name']),
                                    str(r['format']),
                                    str(r['fileName']),
                                    str(last_modified)])

# Genera catalogo de recursos                                              
file = open(f"{'catalogRecursos.csv'}", "a+")
file.write(f"'organizacion';'dataset id';'nombre dataset';'url';'frecuencia actualizacion';'nombre recurso';'formato recurso';'filename';'ultima modificacion'\n")
for recurso in listaRecursos:
    
    for r in recurso:
        file.write(r+';')

    file.write('\n')
