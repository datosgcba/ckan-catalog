import http.server as server
import socketserver
import json
import os,sys,inspect
import pandas as pd
import pickle as cPickle

# Import organizaciones from common
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
data_lib_dir = os.path.join(parent_dir, "complementos/")
sys.path.insert(0,data_lib_dir) 
import catalog_datasets as catalog

class PyJSONHandler(server.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "application/json")
        s.end_headers()
    def do_GET(s):
        """
        Respond to a GET request.
        """
        json_response = json.dumps({'status':'Default response'})
        checkPath = s.path[0:].split('/')
        if(checkPath[1] == ''):
            s.do_ResponseOK(json_response, "application/json")
        else:
            s.do_Header()
    def do_Header(s):
        '''
        Respond only requested header
        '''
        acceptedValues = [
                            'catalog.json',
                            'catalog.xlsx',
                            'catalog.csv'
                        ]

        # Remove first '/' from request string
        requestesHeader = s.path[1:].split('/')
        formato = requestesHeader[0].split('.')
        dict_s = dict(s.headers)
        if str(requestesHeader[0]) in acceptedValues:
            response = catalog.CatalogoDataset()
            s.do_ResponseOK(response, formato[1])
        else:
            json_response = json.dumps({'error':'Value not valid'})
            s.do_ResponseFAIL(json_response)
            
    def do_ResponseOK(s, response, mimetype):
        '''
        Send Response
        '''
        print(type(response))
        df = pd.DataFrame(response, columns=['organizacion','dataset_id','nombre_dataset','url','frecuencia_actualizacion','ultima_modificacion'])
        print(df)
        s.send_response(200)
        s.send_header("Content-type", mimetype)
        s.end_headers()
        if (mimetype=='xlsx'):
            s.send_header('Content-Disposition', 'attachment; filename="catalog.xlsx"')
            df.to_excel('catalog.xlsx', encoding="iso-8859-1", engine='xlsxwriter')
            print(type(df))
            with open('catalog.xlsx', 'rb') as file:
                s.wfile.write(file.read())

        elif (mimetype=='json'):
            df_response = json.dumps(response)
            s.wfile.write(df_response.encode("utf-8"))
        s.end_headers()

    def do_ResponseFAIL(s, response):
        '''
        Send Failed Response
        '''
        s.send_response(400)
        s.send_header("Content-type", "application/json")
        s.end_headers()
        s.wfile.write(response.encode("utf-8"))
        s.end_headers()