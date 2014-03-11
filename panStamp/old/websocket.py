import socket
import time
import threading

def onConnection(mysocket):
	print "waiting for initial communication"
	data = mysocket.recv(1024)
	print data
	print "sending Handshake"
	mysocket.send('''
HTTP/1.1 101 WebSocket Protocol Handshake\r
Date: Fri, 10 Feb 2012 17:38:18 GMT\r
Connection: Upgrade\r
Server: Kaazing Gateway\r
Upgrade: WebSocket\r
Access-Control-Allow-Origin: http://localhost:8000\r
Access-Control-Allow-Credentials: true\r
Sec-WebSocket-Accept: rLHCkw/SKsO9GAH/ZSFhBATDKrU=\r
Access-Control-Allow-Headers: content-type\r
  '''.strip() + '\r\n\r\n')
	print "sending data"
	time.sleep(1)
	mysocket.send('\x00hello\xff')
	time.sleep(1)
	mysocket.send('\x00world\xff')
	print "finished"
	mysocket.close()


print "starting websocket"
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('',8080))
s.listen(1)
while True:
	print "accepting connections"
	liveconnection,addr = s.accept()
	print "connection established by: " + str(addr)
	t1 = threading.Thread(target = onConnection, args = (liveconnection,))
	t1.start()