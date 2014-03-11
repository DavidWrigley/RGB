###############################
# Temperature Sensor MQTT APP #
#       By David Wrigley      #
###############################
import time
import serial
import threading
import json
import mosquitto
import sys

# global vars
global runSerial
global debug
global raw
global t1
global nodeData
global mqttc

# serial read function
def readSerial():
	global runSerial
	global nodeData
	global debug
	global raw
	global mqttc

	ID = 0
	msgNo = 0
	code = 0
	value = 0
	temp = 0.0
	batt = 0.0
	print "Serial thread running"
	while(runSerial):
		data = s.readline()
		if(len(data) > 24):
			try:
				ID = int(data[6:10], 16)
				msgNo = int(data[10:14], 16)
				code = int(data[18:20], 16)
				value = int(data[20:24], 16)
			except:
				print "Incorrect message format / unusefull message"
				pass

			if(raw):
				print "id: " + str(ID) + " msgNo: " + str(msgNo) + " code: " + str(code) + " value: " + str(value)

			# take that data and push it to a list that holds the node data
			if(code == 11):
				batt = (value*.001)
			if(code == 12):
				temp = ((value*.1) - 50)

			if((batt != 0) and (temp != 0)):
				# ready to print
				if(debug):
					# testing
					print "Human Readable: ID: " + str(ID) + ", Temperature: " + str(temp) + " Degrees, Batt: " + str(batt) + "V"
				
				# convert to json
				jsondata = json.dumps({ 'ID' : ID, 'Temp' : temp, 'Batt' : batt })
				if(debug):
					print "json data " + jsondata

				mqttc.publish(conf['mqttdir'], jsondata)
				print "Published"

				# test, decode json data
				jsondatadecode = json.loads(jsondata)
				if(debug):
					for key, value in jsondatadecode.items():
						print key, value

				# set for next run through
				temp = 0
				batt = 0

def start():
	global runSerial
	global t1
	t1 = threading.Thread(target=readSerial)
	if(runSerial == 0):
		# start the thread and serial data
		runSerial = 1
		print "Starting serial thread"
        t1.start()

def stop():
	global runSerial
	print "Joining serial thread, waiting for thread exit"
	runSerial = 0
	t1.join()
	print "Good bye!"

def on_connect(rc):
	if(rc == 0):
		print "Connected to MQTT Server"
	else:
		print "Issue Connecting"

########
# Main #
########

# load configuration
print "loading \"conf.ini\""
try:
	conffile = open("conf.ini", 'r').read()
	conf = json.loads(conffile)
except:
	print "issue reading configuration file, exiting"
	sys.exit()

# init serial port
print "Connecting to serial device"
try:
	s = serial.Serial(port = conf['serialport'], baudrate = 38400) # panStamp
	s.open()
except:
	print "could not connect to device, make sure panStamp is connected and /dev/ttyUSB0 is present"

	# kill the program
	
runSerial = 0
debug = conf['debug']
raw = 0
nodeData = []
mqttc = mosquitto.Mosquitto("python_pub")
mqttc.on_connect = on_connect
mqttc.will_set("/event/dropped", "sorry i have died")

while mqttc.connect(conf['mqttaddr'],conf['mqttport']):
	#print "failed to connect to mqtt on: " + 
	time.sleep(10)

# start the app
run = 1
start()
var = ""
print "\rtype \"stop\" to stop application\n\n"
while(run):
	var = raw_input()
	if(var == "stop"):
		stop()
		run = 0
	if(var == "debug"):
		if(debug):
			print "debug off"
			debug = 0
		else:			
			print "debug on"
			debug = 1
	if(var == "raw"):
		if(raw):
			print "raw data off"
			raw = 0
		else:
			print "raw data on"
			raw = 1
