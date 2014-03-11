########################
#     MQRR Receive 	   #
#   By David Wrigley   #
########################

import mosquitto
import json
import time
import sys
import socket

global mqttc
global mqqtThread
global run
global s

def on_message(mosq, obj, msg):
	global s
	jsondatadecode = json.loads(msg.payload)

	print "ID: " + str(jsondatadecode['ID']) + " Temperature: " + str(jsondatadecode['Temp']) + " Batt: " + str(jsondatadecode['Batt'])

	# send the data
	s.send(msg.payload)
	
def on_connect(self, mosq, obj, rc):
    if(rc == 0):
        print("Connected successfully.")
    else:
    	print("Refused connection.")
    	sys.exit()

########
# Main #
########

print "Starting MQTT Receive"
run = 1

# load configuration
print "loading \"conf.ini\""
try:
	conffile = open("conf.ini", 'r').read()
	conf = json.loads(conffile)
except:
	print "issue reading configuration file, exiting"
	sys.exit()

try:
	mqttc = mosquitto.Mosquitto("python_sub")
	mqttc.will_set("event/dropped", "sorry i have died")
	mqttc.connect(conf['mqttaddr'],conf['mqttport'])
	mqttc.subscribe(conf['mqttdir'], 0)
	mqttc.on_message = on_message

except:
	print "Issues connecting to MQTT server on: " + conf['mqttaddr'] + ":" + str(conf['mqttport'])

print "Starting Socket connection on: " + conf['socketaddr'] + ":" + str(conf['socketport'])

# set up the communication with node.js 
# s should now be used for sending 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

socketconnect = 0

while (socketconnect == 0):
	try:
		s.connect((conf['socketaddr'],conf['socketport']))
		socketconnect = 1
	except:
		print "failed, retrying"
		time.sleep(10)

s.send("hey from python")

while(run):
	# dont exit
	mqttc.loop()
	time.sleep(.5)



