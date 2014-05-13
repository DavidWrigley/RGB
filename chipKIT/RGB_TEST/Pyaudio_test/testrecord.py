"""
PyAudio example: Record a few seconds of audio and save to a WAVE
file.
"""

import pyaudio
import wave
import sys
import numpy as np
import matplotlib.pyplot as plt
import pylab

def downSample(ffty,degree=10):
		y = []
		for i in range(len(ffty)/degree-1):
				y.append(sum(ffty[i*degree:(i+1)*degree])/degree)
		return y

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = .2
WAVE_OUTPUT_FILENAME = "output.wav"

if sys.platform == 'darwin':
	CHANNELS = 1

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
				channels=CHANNELS,
				rate=RATE,
				input=True,
				frames_per_buffer=CHUNK)

frames = []
pylab.show()
pylab.ion()

while True:
	print("* recording")
	pylab.clf()
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		try:
			data = stream.read(CHUNK)
		except IOError:
			print "overflow"
		#print numpy.fromstring(data,dtype=numpy.int16)
		frames.extend((np.fromstring(data,dtype=np.int16)))

	print("* done recording")
	#print frames
	plotdata = np.array(downSample(frames,100))
	pylab.plot(plotdata)
	pylab.draw()
	"""
	plt.plot(downSample(frames,50))
	plt.ylabel('some numbers')
	plt.draw()
	"""
	del(frames)
	frames = []

stream.stop_stream()
stream.close()
p.terminate()

"""
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
"""