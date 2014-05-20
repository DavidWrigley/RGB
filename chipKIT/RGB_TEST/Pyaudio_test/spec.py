#!/usr/bin/env python
# Written by Yu-Jie Lin
# Public Domain
#
# Deps: PyAudio, NumPy, and Matplotlib
# Blog: http://blog.yjl.im/2012/11/frequency-spectrum-of-sound-using.html
 
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
import random as randint
 
SAVE = 0.0
TITLE = ''
FPS = 30.0
 
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
set_point = 30

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
 
  global prev
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

  Y_left = Y[(len(Y)/2):((len(Y)/2)+(len(Y)/4))]

  #print Y_left
  # sum up the bins to be displayed
  average_bins = []
  placeholder = 1
  increment = len(Y_left)/8
  for a in range(0,8):
    average_bins.append(sum(Y_left[placeholder:placeholder+increment]))
    placeholder = placeholder+increment

  #print average_bins

  # calculate the average power
  totalSum = 0
  for a in average_bins:
    totalSum += a

  average_power = totalSum/len(average_bins)
  #print "Average Power: " + str(average_power)

  # create message
  message = ""

  if(len(prev) > 8):
    prev.pop(0)

  colour = [ [8,0,0],
             [8,2,0],
             [4,4,0],
             [0,8,0],
             [0,4,4],
             [0,0,8],
             [3,0,8],
             [8,0,2] ]

  print colour

  # clear previous info
  hist = 0;
  for a in reversed(prev):
    row = 0
    for b in a:
      level = int(round(b/set_point))
      if(level > 7):
        level = 7
      print "hist: %d Level: %d Row: %d" %(hist,level,row)
      message += translate(hist,level,row,0,0,0)
      if(hist < 7):
        message += translate(hist+1,level,row,colour[row][0],colour[row][1],colour[row][2])
      row += 1
    hist += 1

  # display current data on cube
  row = 0
  for a in average_bins:
    level = int(round(a/set_point))
    if(level > 7):
      level = 7
    #print level
    message += translate(0,level,row,colour[row][0],colour[row][1],colour[row][2])
    row += 1

  sendData(message)

  # set previous state
  prev.append(average_bins)
 
  line.set_ydata(Y)
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

  print "clearning cube"
  message = ""
  for a in range(0,8):
    for b in range(0,8):
      for c in range(0,8):
        message += translate(a,b,c,0,0,0)
  sendData(message)

  print "starting visulisation"
  main()