#snake
import socket
import copy
import time
import signal
import sys
import curses
import random
import threading
import termios, fcntl, sys, os

# Socket Varables
TCP_IP = "130.102.86.142"
#TCP_IP = "192.168.1.107"
TCP_PORT = 8888
BUFFER_SIZE = 1024

#global varables
fd = sys.stdin.fileno()
allSnake = []
currentSnake = []
currentPellet = []
score = 0
# x direction y direction z direction
global snakeDirection 

snakeDirection = [0,1,0]
keypress = ''
randomdir = 1
updatetime = .1
randomlimit = .5

layer = 0
pixel = 0
red = 8
green = 8
blue = 8

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

def random_choose():
    while(True):
        print "running random snake"
        timesleep = random.uniform(0,randomlimit)
        time.sleep(timesleep)
        keypress = random.randint(0,6)
        print "sleep: %f, Keypress: %d" %(timesleep,keypress)
        #if its going in the x direction it can go in the y or z
        if(snakeDirection[0] != 0):
            if(keypress == 0):
                # controls y upward direction
                if(snakeDirection[1] == 0):
                    snakeDirection[0] = 0
                    snakeDirection[1] = 1
                    snakeDirection[2] = 0
        
            elif(keypress == 1):
                # controls y downward direction
                if(snakeDirection[1] == 0):
                    snakeDirection[0] = 0
                    snakeDirection[1] = -1
                    snakeDirection[2] = 0

            elif(keypress == 2):
                # controls z positive direction                            
                if(snakeDirection[2] == 0):
                    snakeDirection[0] = 0
                    snakeDirection[1] = 0
                    snakeDirection[2] = 1

            elif(keypress == 3):
                # controls z negative direction                            
                if(snakeDirection[2] == 0):
                    snakeDirection[0] = 0
                    snakeDirection[1] = 0
                    snakeDirection[2] = -1

        #if the snake is going in the y direction can go in x and z
        elif(snakeDirection[1] != 0):
            if(keypress == 2):
                # controls z positive direction                            
                if(snakeDirection[2] == 0):
                    snakeDirection[0] = 0
                    snakeDirection[1] = 0
                    snakeDirection[2] = 1

            elif(keypress == 3):
                # controls z negative direction                            
                if(snakeDirection[2] == 0):
                    snakeDirection[0] = 0
                    snakeDirection[1] = 0
                    snakeDirection[2] = -1
            
            elif(keypress == 4):
                # controls x positive direction                            
                if(snakeDirection[0] == 0):
                    snakeDirection[0] = 1
                    snakeDirection[1] = 0
                    snakeDirection[2] = 0

            elif(keypress == 5):
                # controls z positive direction                            
                if(snakeDirection[0] == 0):
                    snakeDirection[0] = -1
                    snakeDirection[1] = 0
                    snakeDirection[2] = 0

        elif(snakeDirection[2] != 0):
            if(keypress == 4):
                # controls x positive direction                            
                if(snakeDirection[0] == 0):
                    snakeDirection[0] = 1
                    snakeDirection[1] = 0
                    snakeDirection[2] = 0

            elif(keypress == 5):
                # controls z positive direction                            
                if(snakeDirection[0] == 0):
                    snakeDirection[0] = -1
                    snakeDirection[1] = 0
                    snakeDirection[2] = 0

            elif(keypress == 0):
                # controls y upward direction
                if(snakeDirection[1] == 0):
                    snakeDirection[0] = 0
                    snakeDirection[1] = 1
                    snakeDirection[2] = 0
        
            elif(keypress == 1):
                # controls y downward direction
                if(snakeDirection[1] == 0):
                    snakeDirection[0] = 0
                    snakeDirection[1] = -1
                    snakeDirection[2] = 0


def signal_handler(signum, frame):
    """
    Handles the SIGINT signal generated by the keyboard interupt
    ctrl-c
    """
    signal.signal(signal.SIGINT, original_sigint)
    print "joining"
    thread.terminate()
    thread.join()
    print "exiting"
    sys.exit(0)

def ensure_Connect():
    """
    ensures the socket connects with a while loop
    that will not return till 0 is received from the connection
    function (i.e. the socket has not encountered and error)
    """
    while (connect(TCP_IP,TCP_PORT)):
        print "timeout"
    print "connected"

class keyEvent(threading.Thread):

    def __init__(self):
        # initilisation
        self.runvar = 1
        self.oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        self.oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)

        threading.Thread.__init__(self, target=self.run)
    
    def run(self):
        global snakeDirection 
        # key press captucre loop
        try:
            while self.runvar:
                time.sleep(.01)
                try:
                    c = sys.stdin.read(1)
                    #keypress = repr(c)
                    keypress = c
                    print "got: %c" %keypress

                    #if its going in the x direction it can go in the y or z
                    if(snakeDirection[0] != 0):
                        if(keypress == 'i'):
                            # controls y upward direction
                            if(snakeDirection[1] == 0):
                                snakeDirection[0] = 0
                                snakeDirection[1] = 1
                                snakeDirection[2] = 0
                    
                        elif(keypress == 'k'):
                            # controls y downward direction
                            if(snakeDirection[1] == 0):
                                snakeDirection[0] = 0
                                snakeDirection[1] = -1
                                snakeDirection[2] = 0

                        elif(keypress == 'w'):
                            # controls z positive direction                            
                            if(snakeDirection[2] == 0):
                                snakeDirection[0] = 0
                                snakeDirection[1] = 0
                                snakeDirection[2] = 1

                        elif(keypress == 's'):
                            # controls z negative direction                            
                            if(snakeDirection[2] == 0):
                                snakeDirection[0] = 0
                                snakeDirection[1] = 0
                                snakeDirection[2] = -1

                    #if the snake is going in the y direction can go in x and z
                    elif(snakeDirection[1] != 0):
                        if(keypress == 'w'):
                            # controls z positive direction                            
                            if(snakeDirection[2] == 0):
                                snakeDirection[0] = 0
                                snakeDirection[1] = 0
                                snakeDirection[2] = 1

                        elif(keypress == 's'):
                            # controls z negative direction                            
                            if(snakeDirection[2] == 0):
                                snakeDirection[0] = 0
                                snakeDirection[1] = 0
                                snakeDirection[2] = -1
                        
                        elif(keypress == 'd'):
                            # controls x positive direction                            
                            if(snakeDirection[0] == 0):
                                snakeDirection[0] = 1
                                snakeDirection[1] = 0
                                snakeDirection[2] = 0

                        elif(keypress == 'a'):
                            # controls z positive direction                            
                            if(snakeDirection[0] == 0):
                                snakeDirection[0] = -1
                                snakeDirection[1] = 0
                                snakeDirection[2] = 0

                    elif(snakeDirection[2] != 0):
                        if(keypress == 'd'):
                            # controls x positive direction                            
                            if(snakeDirection[0] == 0):
                                snakeDirection[0] = 1
                                snakeDirection[1] = 0
                                snakeDirection[2] = 0

                        elif(keypress == 'a'):
                            # controls z positive direction                            
                            if(snakeDirection[0] == 0):
                                snakeDirection[0] = -1
                                snakeDirection[1] = 0
                                snakeDirection[2] = 0

                        elif(keypress == 'i'):
                            # controls y upward direction
                            if(snakeDirection[1] == 0):
                                snakeDirection[0] = 0
                                snakeDirection[1] = 1
                                snakeDirection[2] = 0
                    
                        elif(keypress == 'k'):
                            # controls y downward direction
                            if(snakeDirection[1] == 0):
                                snakeDirection[0] = 0
                                snakeDirection[1] = -1
                                snakeDirection[2] = 0

                    #print "DIR: %d, %d, %d"  %(snakeDirection[0], snakeDirection[1], snakeDirection[2])
                
                except IOError: 
                    pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, self.oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, self.oldflags)

    def terminate(self):
        # finish the loop
        self.runvar = 0

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

if __name__ == '__main__':
    """
    The main execution thread of the program
    all the magic happens here folks.
    Take user input and convert it to Byte value
    then send it on its way to the microcontroller
    """
    print "start"
    print "preserving lemons"
    # register SIGINT to call back to a gracefull exit function
    original_sigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal_handler)

    # set up the TCP / IP socket so that it has a timeout
    # is reusable and automaticaly binds to a local free port
    print "licking 9v battery"
    sock = socket.socket(socket.AF_INET, # Internet
             socket.SOCK_STREAM) # TCP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(5)
    sock.bind(('',0))

    print "playing with fire"
    # connect the socket to the microcontroller
    ensure_Connect()

    print "multiplying spiders"
    thread = keyEvent()
    thread.start()

    print "clearning play area"

    message = ""
    for a in range(0,8):
        for b in range(0,8):
            for c in range(0,8):
                message += translate(a,b,c,0,0,0)
    sendData(message)

    print "feeding snake"

    #allSnake.append([[2,0,0],[1,0,0],[0,0,0]])
    currentSnake.append([2,0,0])
    currentSnake.append([1,0,0])
    currentSnake.append([0,0,0])
    if(randomdir == 1):
        #allSnake.append([[1,3,7],[3,0,1],[4,1,2]])
        #allSnake.append([[3,6,0],[1,4,2],[2,5,1]])
        #allSnake.append([[3,3,7],[3,2,1],[1,5,3]])
        pass

    print "making pellet"
    currentPellet = [random.randint(0,7),random.randint(0,7),random.randint(0,7)]

    if(randomdir == 1):
        print "randoming"
        target_thread = threading.Thread(target=random_choose)
        target_thread.start()

    while True:
        """
        message = ""
        for a in range(0,8):
            for b in range(0,8):
                for c in range(0,8):
                    message += translate(a,b,c,0,0,0)
        sendData(message)
        """
        message = ""
        # Update the "head" of the snake
        # this little multiplication gets around the stupid mutable feature of 
        # python lits, the dumbest thing in python.
        currentSnake.insert(0,currentSnake[0:1][0]*1)
        
        currentSnake[0][0] += snakeDirection[0]
        currentSnake[0][1] += snakeDirection[1]
        currentSnake[0][2] += snakeDirection[2]

        # wrap cube (overflow)
        if(currentSnake[0][0] > 7):
            currentSnake[0][0] = 0
        if(currentSnake[0][1] > 7):
            currentSnake[0][1] = 0
        if(currentSnake[0][2] > 7):
            currentSnake[0][2] = 0

        # wrap cube (underflow)
        if(currentSnake[0][0] < 0):
            currentSnake[0][0] = 7
        if(currentSnake[0][1] < 0):
            currentSnake[0][1] = 7
        if(currentSnake[0][2] < 0):
            currentSnake[0][2] = 7

        # check for death.
        for i in range(0,len(currentSnake)):
            #pass on the first run through as the head will equal itself
            if(i == 0):
                pass
            else:
                if(currentSnake[0] == currentSnake[i]):
                    print "you died score: %s" %score
                    score = 0
                    del(currentSnake)
                    currentSnake = []
                    currentSnake.append([2,0,0])
                    currentSnake.append([1,0,0])
                    currentSnake.append([0,0,0])
                    currentSnake.append([0,0,0])
                    message = ""
                    for a in range(0,8):
                        for b in range(0,8):
                            for c in range(0,8):
                                message += translate(a,c,b,random.randint(0,8),random.randint(0,8),random.randint(0,8))
                            time.sleep(.01)
                            sendData(message)
                            message = ""

                    message = ""
                    for a in range(0,8):
                        for b in range(0,8):
                            for c in range(0,8):
                                message += translate(a,c,b,0,0,0)
                            sendData(message)
                            message = ""
                    break

        if(currentPellet == currentSnake[0]):
            # if you get the pellet do not zero out the pixel and allow the snake to extend
            # make a new pellet
            currentPellet = [random.randint(0,7),random.randint(0,7),random.randint(0,7)]
            score += 1
            pass
        else:
            # if you dont get a pellet, zero out the last pixel of the snake and pop it off
            message += translate(currentSnake[-1][0],currentSnake[-1][1],currentSnake[-1][2],0,0,0)
            currentSnake.pop()

        for i in range(len(currentSnake)):
            if(i == 0):
                message += translate(currentSnake[i][0],currentSnake[i][1],currentSnake[i][2],0,8,0)
            else:
                message += translate(currentSnake[i][0],currentSnake[i][1],currentSnake[i][2],8,0,0)

        # add the pellet
        message += translate(currentPellet[0],currentPellet[1],currentPellet[2],8,8,8) 
        
        #print currentSnake
        #print message

        # send the data
        sendData(message)
        time.sleep(updatetime)   