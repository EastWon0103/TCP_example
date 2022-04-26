from socket import *
import http.client


HOST = '125.240.96.241'
PORT = 12345

conn = http.client.HTTPConnection(HOST, PORT)
headers = {"Content-type":"aplication/json"}
data = {"data1":123}
conn.request("POST", "/", str(data), headers)
# r = conn.getresponse()
# print(r.status, r.reason)
#print(r.read().decode("utf-8"))

# try:  
#     while True:
#         cmd = input("Request: ")
        
#         request = cmd.split(" ")
#         method = request[0].upper()
#         data = request[1:]

#         headers = {"Content-type":"aplication/json"}


#         if(len(request) == 1):
#             conn.request(method, "/")
#         else:
#             conn.request(method, "/", data, headers) 


        

# except KeyboardInterrupt:
#     print("KeyboardInterrupt: Shutting down the Client")

# finally:
#     conn.close()

conn.close()