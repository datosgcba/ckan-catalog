import http.server as server
import socketserver

class PyHtmlHandler(server.BaseHTTPRequestHandler):
    def do_HEAD(s):
        print("a")
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """
        Respond to a GET request.
        """
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(b"<html><head><title>Title goes here.</title></head>")
        s.wfile.write(b"<body><p>This is a test.</p>")
        s.wfile.write(b"</body></html>")
        s.end_headers()