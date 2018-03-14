
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy.io import wavfile # get the api
from numpy import arange

fs, data = wavfile.read('file.wav') # load the data
a = data.T[0] # this is a two channel soundtrack, I get the first track
b=[(ele/2**8.)*2-1 for ele in a] # this is 8-bit track, b is now normalized on [-1,1)
c = fft(b) # calculate fourier transform (complex numbers list)

#print(abs(max(c)))
d = len(c)//2  # you only need half of the fft list (real signal symmetry)

k = arange(len(data))
T = len(data)/fs  # where fs is the sampling frequency
frqLabel = k/T

val = max(abs(c[2:(d-1)]))
i = list(abs(c[2:(d-1)])).index(val)
print(frqLabel[2:(d-1)][i])

plt.plot(frqLabel[2:(d-1)], abs(c[2:(d-1)]),'r')
plt.show()
