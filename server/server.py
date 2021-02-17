from http.server import HTTPServer, BaseHTTPRequestHandler

class Serv(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self.path = '/index.html'

httpd = HTTPServer(('localhost', 8080), Serv)
print('[SERVER IS STARTING]')
httpd.serve_forever()