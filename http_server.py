import http.server
import socketserver
import codecs
import json
HOST = "125.240.96.241"
PORT = 9999

class MyHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Host IP", HOST)
        self.send_header("Port", str(PORT))
        self.end_headers()
        
    def do_GET(self):
        html_file = codecs.open("index.html", "r", "utf-8")
        lines = html_file.readlines()
        
        try:
            self._set_headers()
            self.wfile.write("".join(lines).encode("utf-8"))
        except Exception as e:
            print(self.error_message_format)
            print(self.error_content_type)
            print(e)
        finally:
            html_file.close()
    
    def do_HEAD(self):
        try:
            self._set_headers()
            self.wfile.write("".encode("utf-8"))
        except Exception as e:
            print(self.error_message_format)
            print(self.error_content_type)
            print(e)
            
    def do_POST(self):
        self._set_headers()
        try:
            data_legth = int(self.headers["Content-Length"])
            data = self.rfile.read(data_legth)
            data = data.decode("utf-8")
            print("받은 데이터: ",data)
            html_data = "                <li>"+data+"</li>\r\n"
            
            f = codecs.open("index.html", "r", "utf-8")
            lines = f.readlines()
            f.close()
            
            f = codecs.open("index.html", "w", "utf-8")
            postable = False
            for i in lines:
                if i.strip() == "</ul>":
                    lines.insert(lines.index(i), html_data)
                    break
                
            f.writelines(lines)
            message = "<" + data +">" + " 등록완료"
            
        except Exception as e:
            print(self.error_message_format)
            print(self.error_content_type)
            print(e)
            message = "<" + data +">" + " 등록실패"
            
        finally:
            self.wfile.write(message.encode("utf-8"))
            f.close()
                
    def do_PUT(self):
        self._set_headers()
        try:
            data_legth = int(self.headers["Content-Length"])
            data = self.rfile.read(data_legth)
            data = data.decode("utf-8")
            data = json.loads(data)
            print("받은 데이터: ",data["old"], data["new"])
            target_data = "                <li>"+data["old"]+"</li>\r\n"
            modify_data = "                <li>"+data["new"]+"</li>\r\n"
            
            f = codecs.open("index.html", "r", "utf-8")
            lines = f.readlines()
            f.close()
            
            target_index = lines.index(target_data)
            lines[target_index] = modify_data

            f = codecs.open("index.html", "w", "utf-8")
            f.writelines(lines)
            message = "<" + data["old"] +" "+"->"+" " + data["new"] +">" + " 수정완료"
        
        except Exception as e:
            print(self.error_message_format)
            print(self.error_content_type)
            print(e)
            message = "<" + data["old"] +" "+"->"+" " + data["new"] +">" + " 수정실패"
            
        finally:
            self.wfile.write(message.encode("utf-8"))
            f.close()
    
    def do_DELETE(self):
        self._set_headers()
        try:
            data_legth = int(self.headers["Content-Length"])
            data = self.rfile.read(data_legth)
            data = data.decode("utf-8")
            print("받은 데이터: ",data)
            target_data = "                <li>"+data+"</li>\r\n"
            
            f = codecs.open("index.html", "r", "utf-8")
            lines = f.readlines()
            f.close()
            
            lines.remove(target_data)
            
            f = codecs.open("index.html", "w", "utf-8")
            f.writelines(lines)
            message = "<" + data +">" + " 삭제완료"
        
        except Exception as e:
            print(self.error_message_format)
            print(self.error_content_type)
            print(e)
            message = "<" + data +">" + " 삭제실패"
            
        finally:
            self.wfile.write(message.encode("utf-8"))
            f.close()
    

with socketserver.TCPServer((HOST, PORT), MyHandler) as httpd:
    try:
        print("serving at ip: ", HOST)
        print("serving at port: ", PORT)
        httpd.serve_forever()
    
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Shutting down the web server")
        httpd.socket.close()
        