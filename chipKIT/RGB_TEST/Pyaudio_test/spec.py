#!/usr/bin/env python
# Written by Yu-Jie Lin
# Public Domain
#
# Deps: PyAudio, NumPy, and Matplotlib
# Blog: http://blog.yjl.im/2012/11/frequency-spectrum-of-sound-using.html
# adapted by David Wrigley
 
import numpy as np
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pyaudio
import struct
import wave
import socket
import time
import math
import random as randint
import threading
import termios, fcntl, sys, os
 
SAVE = 0.0
TITLE = ''
FPS = 60.0
 
#nFFT = 64
nFFT = 512
BUF_SIZE = 4 * nFFT
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
#RATE = 22000

# Socket Varables
TCP_IP = "130.102.86.142"
#TCP_IP = "192.168.1.107"
TCP_PORT = 8888

#previous dft values
global prev
global set_point
global mode
mode = 5
set_point = 6
max_set_point = 40
min_set_point = 1
fd = sys.stdin.fileno()

def cube_reset():
  message = ""
  for a in range(0,8):
    for b in range(0,8):
      for c in range(0,8):
        message += translate(a,b,c,0,0,0)
  sendData(message)

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
    global set_point
    global mode
    # key press captucre loop
    try:
      while self.runvar:
        time.sleep(.01)
        try:
          c = sys.stdin.read(1)
          #keypress = repr(c)
          keypress = c

          # increment / decrement setpoint
          if(keypress == "w"):
            if(set_point < max_set_point):
              set_point += 1
          elif(keypress == "s"):
            if(set_point > min_set_point):
              set_point -= 1

          # Switch mode
          if(keypress == "1"):
            mode = 1
            cube_reset()
            prev = []
          elif(keypress == "2"):
            mode = 2
            cube_reset()
            prev = []
          elif(keypress == "3"):
            mode = 3
            cube_reset()
            prev = []
          elif(keypress == "4"):
            mode = 4
            cube_reset()
            prev = []
          elif(keypress == "5"):
            mode = 5
            cube_reset()
            prev = []
          elif(keypress == "6"):
            mode = 6
            cube_reset()
            prev = []

          print set_point
            
        except IOError: 
            pass
    finally:
      termios.tcsetattr(fd, termios.TCSAFLUSH, self.oldterm)
      fcntl.fcntl(fd, fcntl.F_SETFL, self.oldflags)

  def terminate(self):
      # finish the loop
      self.runvar = 0

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
    try:
      return ( str(unichr(int(yBase[y]))) + str(unichr(int(xBase[x] + zBase[z]))) + str(unichr(int(r))) + str(unichr(int(g))) + str(unichr(int(b))) )
    except TypeError:
      return 

def sendData(data):
    # try to send the message, if failur, then re-connect
    try:
        sock.send(data)
    except socket.error:
        print "disconnected, atempting reconnect"
        ensure_Connect()
        sock.send(data)
 
def animate(i, line, stream, wf, MAX_y):
 
  global prev
  global set_point
  global mode
  # Read n*nFFT frames from stream, n > 0
  N = max(stream.get_read_available() / nFFT, 1) * nFFT
  data = None
  while (data == None):
    try:
      data = stream.read(N)
    except IOError:
      print "overflow"
  if SAVE:
    wf.writeframes(data)
 
  # Unpack data, LRLRLR...
  y = np.array(struct.unpack("%dh" % (N * CHANNELS), data)) / MAX_y
  y_L = y[::2]
  y_R = y[1::2]
 
  Y_L = np.fft.fft(y_L, nFFT)
  Y_R = np.fft.fft(y_R, nFFT)
  
  # Sewing FFT of two channels together, DC part uses right channel's
  Y = abs(np.hstack((Y_L[-nFFT/2:-1], Y_R[:nFFT/2])))

  colour = [ [8,0,0],
               [8,2,0],
               [4,4,0],
               [0,8,0],
               [0,4,4],
               [0,0,8],
               [3,0,8],
               [8,0,2] ]

  if(mode == 1):
    # this mode is complete dft based
    Y_left = Y[(len(Y)/2):-1]
    # print len(Y_left)

    # sum up the bins to be displayed
    average_bins = []
    placeholder = 0
    increment = round(len(Y_left)/64)
    for a in range(0,64):
      average_bins.append(sum(Y_left[placeholder:placeholder+increment]))
      placeholder = placeholder+increment

    message = ""

    # reset the previous frame
    for a in prev:
      message += translate(a[0],a[1],a[2],0,0,0)

    prev = []

    # send new frame
    bin = 0
    for x in range(0,8):
      for z in range(0,8):
          level = int(round(average_bins[bin]/set_point))
          if( level > 7):
            level = 7
          if level == 0:
            setcolour = colour[0]
          elif level == 1:
            setcolour = colour[1]
          elif level == 2:
            setcolour = colour[2]
          elif level == 3:
            setcolour = colour[3]
          elif level == 4:
            setcolour = colour[4]
          elif level == 5:
            setcolour = colour[5]
          elif level == 6:
            setcolour = colour[6]
          elif level == 7:
            setcolour = colour[7]
          message += translate(x,level,z,8,0,3)
          prev.append([x,level,z])
          bin += 1

    sendData(message)
  
  elif(mode == 2):
    # this mode is complete dft based
    Y_left = Y[(len(Y)/2)-1:(len(Y)/2 + len(Y)/4)]
    # print len(Y_left)

    # sum up the bins to be displayed
    average_bins = []
    placeholder = 0
    increment = round(len(Y_left)/64)
    for a in range(0,64):
      average_bins.append(sum(Y_left[placeholder:placeholder+increment]))
      placeholder = placeholder+increment

    message = ""

    # reset the previous frame
    for a in prev:
      message += translate(a[0],a[1],a[2],0,0,0)

    prev = []

    # send new frame
    bin = 0
    for x in range(0,8):
      for z in range(0,8):
          level = int(round(average_bins[bin]/set_point))
          if( level > 7):
            level = 7
          if level == 0:
            setcolour = colour[0]
          elif level == 1:
            setcolour = colour[1]
          elif level == 2:
            setcolour = colour[2]
          elif level == 3:
            setcolour = colour[3]
          elif level == 4:
            setcolour = colour[4]
          elif level == 5:
            setcolour = colour[5]
          elif level == 6:
            setcolour = colour[6]
          elif level == 7:
            setcolour = colour[7]
          message += translate(x,level,z,setcolour[0],setcolour[1],setcolour[2])
          prev.append([x,level,z])
          bin += 1

    sendData(message)

  elif(mode == 3):
    # this mode is complete dft based
    Y_left = Y[(len(Y)/2)-1:(len(Y)/2 + len(Y)/4)]
    # print len(Y_left)

    # sum up the bins to be displayed
    average_bins = []
    placeholder = 0
    increment = round(len(Y_left)/64)
    for a in range(0,64):
      average_bins.append(sum(Y_left[placeholder:placeholder+increment]))
      placeholder = placeholder+increment

    message = ""

    # reset the previous frame
    for a in prev:
      message += translate(a[0],a[1],a[2],0,0,0)

    prev = []

    # send new frame
    bin = 0
    for x in range(0,8):
      for z in range(0,8):
          level = int(round(average_bins[bin]/set_point))
          for a in range(level-1,-1,-1):
            if( a > 7):
              a = 7
            if a == 0:
              setcolour = colour[0]
            elif a == 1:
              setcolour = colour[1]
            elif a == 2:
              setcolour = colour[2]
            elif a == 3:
              setcolour = colour[3]
            elif a == 4:
              setcolour = colour[4]
            elif a == 5:
              setcolour = colour[5]
            elif a == 6:
              setcolour = colour[6]
            elif a == 7:
              setcolour = colour[7]
            message += translate(x,a,z,setcolour[0],setcolour[1],setcolour[2])
            prev.append([x,a,z])
          bin += 1

    sendData(message)

  elif(mode == 4):
    # this mode is complete dft based
    Y_left = Y[(len(Y)/2):-1]

    # sum up the bins to be displayed
    average_bins = []
    placeholder = 0
    increment = round(len(Y_left)/64)
    for a in range(0,64):
      average_bins.append(sum(Y_left[placeholder:placeholder+increment]))
      placeholder = placeholder+increment

    message = ""

    # reset the previous frame
    for a in prev:
      message += translate(a[0],a[1],a[2],0,0,0)

    prev = []
    # send new frame
    bin = 0

    # this will get you to the diagonal
    for x in range(0,8):
      for z in range(0,x+1):
          level = int(round(average_bins[bin]/set_point))
          if( level > 7):
            level = 7
          message += translate((x-z),level,z,0,8,1)
          prev.append([(x-z),level,z])
          bin += 1

    for rows in range(1,8):
      count = 0
      for z in range(rows,8):
          level = int(round(average_bins[bin]/set_point))
          if( level > 7):
            level = 7
          message += translate((7-count),level,z,0,8,1)
          prev.append([(7-count),level,z])
          bin += 1
          count += 1

    sendData(message)

  elif(mode == 5):
    # this mode is complete dft based
    Y_left = Y[(len(Y)/2)-1:(len(Y)/2 + len(Y)/4)]

    # sum up the bins to be displayed
    average_bins = []
    placeholder = 0
    increment = round(len(Y_left)/64)
    for a in range(0,64):
      average_bins.append(sum(Y_left[placeholder:placeholder+increment]))
      placeholder = placeholder+increment

    message = ""

    # reset the previous frame
    for a in prev:
      message += translate(a[0],a[1],a[2],0,0,0)

    # reset prev frame, only hold one frame at a time
    prev = []
    # send new frame
    bin = 0

    # this will get you to the diagonal
    for x in range(0,8):
      for z in range(0,x+1):
          level = int(round(average_bins[bin]/set_point))
          if( level > 7):
            level = 7
          if level == 0:
            setcolour = colour[0]
          elif level == 1:
            setcolour = colour[1]
          elif level == 2:
            setcolour = colour[2]
          elif level == 3:
            setcolour = colour[3]
          elif level == 4:
            setcolour = colour[4]
          elif level == 5:
            setcolour = colour[5]
          elif level == 6:
            setcolour = colour[6]
          elif level == 7:
            setcolour = colour[7]
          message += translate((x-z),level,z,setcolour[0],setcolour[1],setcolour[2])
          prev.append([(x-z),level,z])
          bin += 1

    # need to do the other half of the triangle
    for rows in range(1,8):
      count = 0
      for z in range(rows,8):
          level = int(round(average_bins[bin]/set_point))
          if( level > 7):
            level = 7
          if level == 0:
            setcolour = colour[0]
          elif level == 1:
            setcolour = colour[1]
          elif level == 2:
            setcolour = colour[2]
          elif level == 3:
            setcolour = colour[3]
          elif level == 4:
            setcolour = colour[4]
          elif level == 5:
            setcolour = colour[5]
          elif level == 6:
            setcolour = colour[6]
          elif level == 7:
            setcolour = colour[7]
          message += translate((7-count),level,z,setcolour[0],setcolour[1],setcolour[2])
          prev.append([(7-count),level,z])
          bin += 1
          count += 1

    sendData(message)


  elif(mode == 6):
    # this mode is complete dft based
    Y_left = Y[(len(Y)/2)-1:(len(Y)/2 + len(Y)/4)]

    # sum up the bins to be displayed
    average_bins = []
    placeholder = 0
    increment = round(len(Y_left)/64)
    for a in range(0,64):
      average_bins.append(sum(Y_left[placeholder:placeholder+increment]))
      placeholder = placeholder+increment

    message = ""

    # reset the previous frame
    for a in prev:
      message += translate(a[0],a[1],a[2],0,0,0)

    # reset prev frame, only hold one frame at a time
    prev = []
    # send new frame
    bin = 0

    # this will get you to the diagonal
    for x in range(0,8):
      for z in range(0,x+1):
          level = int(round(average_bins[bin]/set_point))
          for a in range(level-1,-1,-1):
            if( a > 7):
              a = 7
            if a == 0:
              setcolour = colour[0]
            elif a == 1:
              setcolour = colour[1]
            elif a == 2:
              setcolour = colour[2]
            elif a == 3:
              setcolour = colour[3]
            elif a == 4:
              setcolour = colour[4]
            elif a == 5:
              setcolour = colour[5]
            elif a == 6:
              setcolour = colour[6]
            elif a == 7:
              setcolour = colour[7]
            message += translate((x-z),a,z,setcolour[0],setcolour[1],setcolour[2])
            prev.append([(x-z),a,z])
          bin += 1

    # need to do the other half of the triangle
    for rows in range(1,8):
      count = 0
      for z in range(rows,8):
          level = int(round(average_bins[bin]/set_point))
          for a in range(level-1,-1,-1):
            if( a > 7):
              a = 7
            if a == 0:
              setcolour = colour[0]
            elif a == 1:
              setcolour = colour[1]
            elif a == 2:
              setcolour = colour[2]
            elif a == 3:
              setcolour = colour[3]
            elif a == 4:
              setcolour = colour[4]
            elif a == 5:
              setcolour = colour[5]
            elif a == 6:
              setcolour = colour[6]
            elif a == 7:
              setcolour = colour[7]
            message += translate((7-count),a,z,setcolour[0],setcolour[1],setcolour[2])
            prev.append([(7-count),a,z])
          bin += 1
          count += 1

    sendData(message)
 
  #line.set_ydata(Y)
  return line,
 
def init(line):
 
  # This data is a clear frame for animation
  line.set_ydata(np.zeros(nFFT - 1))
  return line,
 
 
def main():
  
  fig = plt.figure()
 
  # Frequency range
  x_f = 1.0 * np.arange(-nFFT / 2 + 1, nFFT / 2) / nFFT * RATE
  ax = fig.add_subplot(111, title=TITLE, xlim=(x_f[0], x_f[-1]),
                       ylim=(0, 1 * np.pi * nFFT**2 / RATE))
  ax.set_yscale('symlog', linthreshy=nFFT**0.5)
 
  line, = ax.plot(x_f, np.zeros(nFFT - 1))
 
  # Change x tick labels for left channel
  def change_xlabel(evt):
    labels = [label.get_text().replace(u'\u2212', '')
              for label in ax.get_xticklabels()]
    ax.set_xticklabels(labels)
    fig.canvas.mpl_disconnect(drawid)
  drawid = fig.canvas.mpl_connect('draw_event', change_xlabel)
 
  p = pyaudio.PyAudio()
  # Used for normalizing signal. If use paFloat32, then it's already -1..1.
  # Because of saving wave, paInt16 will be easier.
  MAX_y = 2.0**(p.get_sample_size(FORMAT) * 8 - 1)
 
  frames = None
  wf = None
  if SAVE:
    frames = int(FPS * SAVE)
    wf = wave.open('temp.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
 
  stream = p.open(format=FORMAT,
                  channels=CHANNELS,
                  rate=RATE,
                  input=True,
                  frames_per_buffer=BUF_SIZE)

  N = max(stream.get_read_available() / nFFT, 1) * nFFT
  print N
  data = stream.read(N)
 
  ani = animation.FuncAnimation(fig, animate, frames,
      init_func=lambda: init(line), fargs=(line, stream, wf, MAX_y),
      interval=1000.0/FPS, blit=True)
 
  if SAVE:
    ani.save('temp.mp4', fps=FPS)
  else:
    plt.show()
 
  stream.stop_stream()
  stream.close()
  p.terminate()
 
  if SAVE:
    wf.close()
 
 
if __name__ == '__main__':
  prev = []
  print "Connecting to Cube"
  sock = socket.socket(socket.AF_INET, # Internet
      socket.SOCK_STREAM) # TCP
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.settimeout(5)
  sock.bind(('',0))

  print "TCP"
  # connect the socket to the microcontroller
  ensure_Connect()

  print "multiplying spiders"
  thread = keyEvent()
  thread.start()

  print "clearning cube"
  cube_reset()

  print "starting visulisation"
  main()