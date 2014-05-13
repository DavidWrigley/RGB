import pyaudio
import scipy
import numpy
import struct
import scipy.fftpack
import matplotlib.pyplot as plt

import threading
import time, datetime
import math

import matplotlib
matplotlib.use('TkAgg')

#ADJUST THIS TO CHANGE SPEED/SIZE OF FFT
bufferSize=1024
#bufferSize=2**8

# ADJUST THIS TO CHANGE SPEED/SIZE OF FFT
sampleRate=44100 
#sampleRate=16000

p = pyaudio.PyAudio()
chunks=[]
ffts=[]
def stream():
		global chunks, inStream, bufferSize
		while True:
			try:
				chunks.append(inStream.read(bufferSize))
			except IOError:
				print "overflow"

def record():
		global w, inStream, p, bufferSize
		inStream = p.open(format=pyaudio.paInt16,channels=1,\
				rate=sampleRate,input=True,frames_per_buffer=bufferSize)
		threading.Thread(target=stream).start()

def downSample(fftx,ffty,degree=10):
		x,y=[],[]
		for i in range(len(ffty)/degree-1):
				x.append(fftx[i*degree+degree/2])
				y.append(sum(ffty[i*degree:(i+1)*degree])/degree)
		return [x,y]

def smoothWindow(fftx,ffty,degree=10):
		lx,ly=fftx[degree:-degree],[]
		for i in range(degree,len(ffty)-degree):
				ly.append(sum(ffty[i-degree:i+degree]))
		return [lx,ly]

def smoothMemory(ffty,degree=3):
		global ffts
		ffts = ffts+[ffty]
		if len(ffts) <= degree: return ffty
		ffts=ffts[1:]
		return scipy.average(scipy.array(ffts),0)

def detrend(fftx,ffty,degree=10):
		lx,ly=fftx[degree:-degree],[]
		for i in range(degree,len(ffty)-degree):
				ly.append(ffty[i]-sum(ffty[i-degree:i+degree])/(degree*2))
				#ly.append(fft[i]-(ffty[i-degree]+ffty[i+degree])/2)
		return [lx,ly]

def graph():
		global chunks, bufferSize, fftx,ffty, w
		if len(chunks)>0:
				data = chunks.pop(0)
				data=scipy.array(struct.unpack("%dB"%(bufferSize*2),data))
				#print "RECORDED",len(data)/float(sampleRate),"SEC"
				ffty=abs(scipy.fftpack.fft(data))
				fftx=scipy.fftpack.rfftfreq(bufferSize*2, 1.0/sampleRate)
				#fftx=fftx[0:len(fftx)/4]
				#ffty=abs(ffty[0:len(ffty)/2])/1000
				ffty=abs(ffty[0:len(ffty)/2])/250
				fftx=fftx[0:len(fftx)/4]*4
				ffty1=ffty[:len(ffty)/2]
				ffty2=ffty[len(ffty)/2::] #+2
				ffty2=ffty2[::-1]
				ffty=ffty1+ffty2              
				#ffty=scipy.log(ffty)-2
				#fftx,ffty=downSample(fftx,ffty,2)
				#print "len of y: %d len of x: %d" %(len(ffty),len(fftx))
				fftx,ffty=detrend(fftx,ffty,10)
				#fftx,ffty=smoothWindow(fftx,ffty,2)
				#ffty=smoothMemory(ffty,3)
				#fftx,ffty=detrend(fftx,ffty,10) 
				# print ffty
				print "graphing"
				plt.clf()      
				#absdft = abs(ffty[0:len(ffty)])
				plt.plot(fftx[10:],20*scipy.log10(ffty[10:]))

				plt.draw()
				print "done"
		if len(chunks)>20:
				print "dropping chunks...",len(chunks)
				chunks = []

def go(x=None):
		global w,fftx,ffty
		print "STARTING!"
		plt.plot([1])
		plt.ylabel('Amp')
		plt.xlabel('Frequency')
		plt.show(block=False)
		threading.Thread(target=record).start()
		while True:
				graph()
		
go()