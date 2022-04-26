import http.server
import socketserver
import codecs
HOST = "125.240.96.241"
PORT = 12345

class MyHandler(http.server.BaseHTTPRequestHandler):
    
    def do_GET(self):
        html_file = codecs.open("index.html", "r", "utf-8")
        lines = html_file.readlines()
        
        try:
            self.send_response(200)
            self.send_header("Content-Type", 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("".join(lines).encode("utf-8"))
        except Exception:
            print(self.error_message_format)
            print(self.error_content_type)
            print("error")
        finally:
            html_file.close()
    
    def do_HEAD(self):
        try:
            self.send_response(200)
            self.send_header("Content-Type", 'text/html; charset=utf-8')
            self.end_headers()
        except:
            print("hi")
            
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        
        data_legth = int(self.headers["Content-Length"])
        data = self.rfile.read(data_legth)
        print(type(data))    
    
    def do_PUT(self):
        self.send_response(200)
    
    def do_DELETE(self):
        self.send_response(200)
    
    

with socketserver.TCPServer((HOST, PORT), MyHandler) as httpd:
    try:
        print("serving at ip: ", HOST)
        print("serving at port: ", PORT)
        httpd.serve_forever()
    
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Shutting down the web server")
        httpd.socket.close()
        