import http.server, socketserver

class CORSHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

with socketserver.TCPServer(('', 8081), CORSHandler) as httpd:
    print('Serving with CORS on port 8081...')
    httpd.serve_forever()