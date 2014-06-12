import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pyaudio
import struct
import socket
import time
from random import randint

# Socket Varables
TCP_IP = "130.102.86.142"
#TCP_IP = "192.168.1.107"
TCP_PORT = 8888

SAVE = 0.0
TITLE = 'current envelope'
FPS = 60

setPoint = .01
mode = 3

SIZE = 125
BUF_SIZE = SIZE * 4
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

def connect(IP, Port):
    """
    Connects a TCP/IP socket to the entered IP and Port
    """
    try:
        sock.connect((TCP_IP, TCP_PORT))
        return 0
    except socket.timeout:
        time.sleep(4)
        return 1

def ensure_Connect():
    """
    ensures the socket connects with a while loop
    that will not return till 0 is received from the connection
    function (i.e. the socket has not encountered and error)
    """
    while (connect(TCP_IP,TCP_PORT)):
        print "timeout"
    print "connected"

def translate(x,y,z,r,g,b):
    # x will be pixels along the front face
    # 0 8 16 24 32 40 48 56 pixels
    xBase = [0, 8, 16, 24, 32, 40, 48, 56]

    # y will be layers 
    # 0 1 2 3 4 5 6 7 layers
    yBase = [0, 1, 2, 3, 4, 5, 6, 7]

    # z will be pixels
    # 0 1 2 3 4 5 6 7
    zBase = [0, 1, 2, 3, 4, 5, 6, 7]

    #print "Layer: %d Pixel: %d R: %d G: %d B: %d" %(yBase[y], (xBase[x]+zBase[z]), r, g, b)
    return ( str(unichr(int(yBase[y]))) + str(unichr(int(xBase[x] + zBase[z]))) + str(unichr(int(r))) + str(unichr(int(g))) + str(unichr(int(b))) )

def sendData(data):
    # try to send the message, if failur, then re-connect
    try:
        sock.send(data)
    except socket.error:
        print "disconnected, atempting reconnect"
        ensure_Connect()
        sock.send(data)

def animate(i, line, stream, wf, MAX_y):
	#print "getting data"
	N = max(stream.get_read_available() / SIZE,1) * SIZE
	data = None
	while (data == None):
		try:
			data = stream.read(N)
		except IOError:
			#print "Overflow"
			pass

	# unpack
	y = np.array(struct.unpack("%dh" % (N * CHANNELS), data)) / MAX_y

	line.set_data(np.arange(0,len(y)),y)

	if(mode == 2):
		# pulse
		message = ""
		#fixed block x,y,z
		colour = [randint(0,8),randint(0,8),randint(0,8)]
		value = round(max(y)*33)
		limiter = 0
		scale = 3

		print "Value: " + str(value)

		if(value > 7.0):
			limiter = 7
		else:
			limiter = int(value)
		
		
		for a in range(7,6-limiter,-1):
			for b in range(0,limiter+1,1):
				for c in range(7,6-limiter,-1):
					message += translate(b,a,c,colour[0],colour[1],colour[2])

		sendData(message)
	elif(mode == 3):
		# pulse
		message = ""
		#fixed block x,y,z
		colour = [randint(0,8),randint(0,8),randint(0,8)]
		value = round(max(y)*16)
		limiter = 0
		scale = 3

		print "Value: " + str(value)

		if(value > 4.0):
			limiter = 4
		else:
			limiter = int(value)
		
		for a in range(3+limiter,3-limiter,-1):
			for b in range(3+limiter,3-limiter,-1):
				for c in range(3+limiter,3-limiter,-1):
					message += translate(b,a,c,colour[0],colour[1],colour[2])

		sendData(message)

	if(max(y) > setPoint):
		#pick a mode
		if(mode == 0):
			# random star
			message = ""
			point = [randint(1,6),randint(1,6),randint(1,6)]
			colour = [randint(0,8),randint(0,8),randint(0,8)]
			for a in range(-1,2):
				message += translate((point[0] + a),(point[1]),(point[2]),colour[0],colour[1],colour[2])
			for a in range(-1,2):
				message += translate((point[0]),(point[1] + a),(point[2]),colour[0],colour[1],colour[2])
			for a in range(-1,2):
				message += translate((point[0]),(point[1]),(point[2] + a),colour[0],colour[1],colour[2])
		elif(mode == 1):
			# random square
			message = ""
			point = [randint(1,6),randint(1,6),randint(1,6)]
			colour = [randint(0,8),randint(0,8),randint(0,8)]
			for a in range(-1,2):
				for b in range(-1,2):
					for c in range(-1,2):
						message += translate((point[0] + a),(point[1] + b),(point[2] + c),colour[0],colour[1],colour[2])

		sendData(message)

	return line,

def init(line):

	line.set_ydata(np.zeros(4000))
	return line,

def main():
	fig = plt.figure()

	# X axis
	ax = fig.add_subplot(111, title=TITLE)

	ax.set_yscale('symlog', linthreshy=SIZE**.05)

	#print "xaxis: %d yaxis: %d" %(len(x_axis), len(np.zeros(SIZE)))
	line, = ax.plot(np.arange(0,4000), np.zeros(4000))

	def change_xlabel(evt):
		labels = [label.get_text().replace(u'\u2212', '')
              for label in ax.get_xticklabels()]
		ax.set_xticklabels(labels)
		fig.canvas.mpl_disconnect(drawid)
	drawid = fig.canvas.mpl_connect('draw_event', change_xlabel)

	p = pyaudio.PyAudio()

	MAX_y = 2.0**(p.get_sample_size(FORMAT) * 9 - 1)
	frames = None
	wf = None

	stream = p.open(format = FORMAT,
					channels = CHANNELS,
					rate = RATE,
					input = True,
					frames_per_buffer = BUF_SIZE)

	N = max(stream.get_read_available() / SIZE,1) * SIZE
	data = stream.read(N)

	ani = animation.FuncAnimation(fig, animate, frames,
		init_func = lambda: init(line), fargs = (line, stream, wf, MAX_y),
		interval = 1000.0/FPS, blit = True)

	plt.show()

	#while True:
	#	pass

	stream.stop_stream()
	stream.close()
	p.terminate()

if __name__ == '__main__':
	print "Connecting to Cube"
	sock = socket.socket(socket.AF_INET, # Internet
			socket.SOCK_STREAM) # TCP
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.settimeout(5)
	sock.bind(('',0))

	print "TCP"
	# connect the socket to the microcontroller
	ensure_Connect()

	print "clearning cube"
	message = ""
	for a in range(0,8):
		for b in range(0,8):
			for c in range(0,8):
				message += translate(a,b,c,0,0,0)
	sendData(message)

	print "starting visulisation"
	main()
