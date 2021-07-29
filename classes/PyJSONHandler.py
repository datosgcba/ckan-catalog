import http.server as server
from io import StringIO
import socketserver
import json
import os,sys,inspect
import pandas as pd
import pickle as cPickle
import csv

from pandas.core.frame import DataFrame

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
        json_response = json.dumps({'status':'Missing Parameter'})
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
        print(requestesHeader[0])
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
        s.send_response(200)
        empty_request = False
        if (isinstance(response, str) and 'Missing Parameter' in response ):
            empty_request = True
        if (empty_request):
            s.send_header("Content-type", "application/json")
            s.end_headers()
            s.wfile.write(response.encode("utf-8"))
        else:
          dataFrame = pd.DataFrame(response, columns=['organizacion','dataset_id','nombre_dataset','url','frecuencia_actualizacion','ultima_modificacion'])
          df = dataFrame.set_index('organizacion')
          
          if (mimetype=='xlsx'):
            s.end_headers()
            s.send_header('Content-Disposition', 'attachment; filename="catalog.xlsx"')
            df.to_excel('catalog.xlsx', encoding="iso-8859-1", engine='xlsxwriter')
            with open('catalog.xlsx', 'rb') as file:
                s.wfile.write(file.read())
          
          elif (mimetype=='csv'):
            # Create an in-memory text stream
            textStream = StringIO()

            # Write the DataFrame contents to the text stream's buffer as a CSV
            df.to_csv(textStream)
            csv = textStream.getvalue()
            print("DataFrame as CSV (from the buffer):")
            
            # Print the buffer contents
            s.end_headers()
            s.send_header('Content-Disposition', 'attachment; filename="catalog.csv"')
            s.wfile.write(csv.encode("utf-8"))
                            
          
          elif (mimetype=='json'):
            df_response = json.dumps(response)
            s.send_header("Content-type", "application/json")
            s.end_headers()
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