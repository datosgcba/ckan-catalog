import http.server as server
import socketserver
import os,sys,inspect

PORT = 8000

# Import classes and Handlers
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
classes_dir = os.path.join(current_dir, "classes")
sys.path.insert(0,classes_dir) 

from PyJSONHandler import PyJSONHandler as pyJSONHandler


def run(server_class=server.HTTPServer, handler_class=pyJSONHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()