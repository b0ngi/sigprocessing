#!/usr/bin/env python
# coding: utf-8

# ## Import Libraries

# In[1]:

import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read, write
from PIL import Image


from numpy.fft import fft, ifft


# ## Read Audio Input "Neural Network"

# You can use scipy.io.wavefile to read and write a wav file.
# Usually audio file contains two channels (left and right). We will only keep one channel for simplicity. In the code below, "data = data[:,0]" will keep channel 0.
#
# The duration of the audio can be calculated as:
#
# $time_{length}=N/F_s$
# - Where N is the number of samples
# - F_s is the sampling rate

# In[2]:

if len(sys.argv) < 2:
    print("please provide a wav file")
    exit()
file = sys.argv[1]

Fs_NN0, data_NN0 = read(file)
data_NN0=data_NN0[:]
N=len(data_NN0)
t_length=N/Fs_NN0
time=np.linspace(0,t_length,N)
# Plot the wave
plt.figure()
plt.plot(time,data_NN0)
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.title('Waveform of Test Audio')
plt.show()
#Play the audio with  IPython.display.Audio
# Audio(data_NN0, rate=Fs_NN0)

print("please provide slicing times in seconds")
sigstart_seconds = float(input("start of signal: "))
sigstop_seconds = float(input("end of signal: "))

sigstart = int(sigstart_seconds * Fs_NN0)
sigstop = int((sigstop_seconds - t_length) * Fs_NN0)

# ## Get the spectrum

# In[3]:


# for opening the media file
import scipy.io.wavfile as wavfile

# powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram(data_NN0, Fs=Fs_NN0)
# plt.show()


# # Remove deadzones

# In[4]:


Fs_NN0, data_NN0 = read(file)

data_NN0=data_NN0[sigstart:sigstop]

#Get the time vector
N=len(data_NN0)
t_length=N/Fs_NN0
time=np.linspace(0,t_length,N)

# Plot the wave
plt.figure()
plt.plot(time,data_NN0)
plt.xlabel('Sample Index')
plt.ylabel('Amplitude')
plt.title('Waveform of Test Audio')
plt.show()
#Play the audio with  IPython.display.Audio
# Audio(data_NN0, rate=Fs_NN0)

# ## Get the spectrum new signal

# In[5]:


# fig, (ax1, ax2) = plt.subplots(nrows=2,figsize=(10, 8))
# ax1.plot(time,data_NN0)


NFFT = 256  # the length of the windowing segments
powerSpectrum, frequenciesFound, time, imageAxis = plt.specgram( data_NN0, NFFT=NFFT, Fs=Fs_NN0, noverlap=128)
# The `specgram` method returns 4 objects. They are:
# - Pxx: the periodogram
# - freqs: the frequency vector
# - bins: the centers of the time bins
# - im: the matplotlib.image.AxesImage instance representing the data in the plot

# plt.show()

fname = file + '-spectrogram.png'
fnamegs = file + '-greyscale.png'
fnamefinal = file + '-image.png'
#Save the image

plt.axis('off')
plt.savefig(fname, bbox_inches='tight',pad_inches = 0)
#Convert the image into grayscale
img = Image.open(fname).convert('L')
img.save(fnamegs)
#Resize
image = Image.open(fnamegs)
new_image = image.resize((435, 300))
new_image.save(fnamefinal)
