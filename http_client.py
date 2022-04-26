import http.client
import json


HOST = "125.240.96.241"
PORT = 12345

conn = http.client.HTTPConnection(HOST, PORT)
headers = {"Content-type":"text/html"}
# data = {"data1":123}
# conn.request("POST", "/", str(data), headers)

try:
    while True:
        cmd = input("명령어 입력: ")
        cmd = cmd.upper()
        
        # HTTP REQUEST: GET
        # html을 텍스트로 돌려받고 터미널에서 todolist를 확인가능        
        if cmd == "GET":
            conn.request(cmd, "/")
            r = conn.getresponse()
            print(r.status, r.reason)
            toDoList = []
            for i in r.readlines():
                txt = i.decode("utf-8")
                print(txt, end="")         
                if txt.strip()[:4] == "<li>":
                    txt = txt.strip()[4:]
                    txt = txt.strip()[:len(txt)-5]
                    toDoList.append(txt)
                    
            print("\n")
            print("To Do List")
            for todo in toDoList:
                print("* "+todo)    
            print()
        
        # HTTP REQUEST: HEAD
        # header의 간단한 부분만 살펴볼 수 있다.  
        elif cmd == "HEAD":
            conn.request(cmd, "/")
            r = conn.getresponse()
            print(r.headers)
        
        # HTTP REQUEST: POST
        # 데이터 등록하기 
        elif cmd == "POST":
            data = input("등록할 데이터: ")
            conn.request(cmd, "/", data.encode("utf-8"),headers)
            r = conn.getresponse()
            print(r.status, r.reason)
            print(r.read().decode("utf-8"))
            print()

        elif cmd == "DELETE":
            data = input("삭제할 데이터: ")
            conn.request(cmd, "/", data.encode("utf-8"),headers)
            r = conn.getresponse()
            print(r.status, r.reason)
            print(r.read().decode("utf-8"))
            print()
        
        elif cmd == "PUT":
            mData = input("수정할 데이터: ")
            nData = input("바꿀 내용: ")
            
            data = {"old": mData, "new": nData}
            
            conn.request(cmd, "/", json.dumps(data).encode("utf-8"), {"Content-type":"application/json"})
            r = conn.getresponse()
            print(r.status, r.reason)
            print(r.read().decode("utf-8"))
            print()
            
        else:
            print("잘못된 명령어")
            print()
            continue

except KeyboardInterrupt:
    print("KeyboardInterrupt: 서버를 종료합니다.")

except Exception as e:
    print(e, ": shutting down client program")
    
finally:
    conn.close()