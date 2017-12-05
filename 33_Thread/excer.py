import requests
import websocket

# res = requests.get("http://open.douyucdn.cn/api/RoomApi/live/lol")
# data = res.json()
# print(data)
socket = websocket.WebSocket()
# socket.connect("ws://36.110.220.49:7533/ws?v=17.07.10.01&p=1&n=1&r=188065&d=7513e65ecdc362f23c0338e2a176dcfb&at=3&ak=7513e65ecdc362f23c0338e2a176dcfb&ag=1&sg=5967bf44ecdb0dc893bdf4a61351ec67")
socket.connect("ws://36.110.220.49:7533/ws?v=17.07.10.01&p=1&n=1&r=134147&d=7513e65ecdc362f23c0338e2a176dcfb&at=3&ak=7513e65ecdc362f23c0338e2a176dcfb&ag=1&sg=533a44c7941855026918cb700a2ebda3")

while 1:
    data = socket.recv()
    print ("data is", data)
# print(data['data'])