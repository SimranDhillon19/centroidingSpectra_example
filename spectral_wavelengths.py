import numpy as np 
import matplotlib.pyplot as plt
%matplotlib inline
plt.rcParams['figure.figsize'] = (20.0, 10.0)
#Load up neon spectrum 
pixels = np.loadtxt('neon.txt',usecols=(0,)) #take zeroth column
signal = np.loadtxt('neon.txt',usecols=(1,)) #take first column

plt.plot(pixels,signal)
plt.xlabel('Pixel Value')
plt.ylabel('Signal')
plt.show()

threshhold = 30000 
peaks = [] 
for i in range(len(signal)-1):
    if (signal[i] > signal[i+1]) and (signal[i]>signal[i-1]) and (signal[i]>threshhold):
        if (signal[i] > signal[i-2]) and (signal[i] > signal[i+2]):
            peaks.append(i)
            
centroids = [] #Values for all the centroids
for i in peaks:
    #Calculate how far backward and forward to go:
    half_max = signal[i] / 2.
    xmin = (np.where(signal[i::-1] < half_max)[0])[0]
    xmax = (np.where(signal[i:] < half_max)[0])[0]
    x_range = pixels[i-xmin:i+xmax]
    I_range = signal[i-xmin:i+xmax]
    x_range = np.array(x_range)
    I_range = np.array(I_range)
    xcm = np.sum((x_range*I_range)) / np.sum(I_range)
    centroids.append(xcm) 
    
def plot_vert(x): 
    '''
    Just plots vertical lines, in blue dashes
    '''
    plt.axvline(x, color='blue', ls='-.')
    
for i in centroids[1:]: #Call my plotting function on every centroid except the first
    plot_vert(i)
    
plt.axvline(centroids[0],color='blue',ls='-.',label='Centroid') 
plt.plot(pixels, signal, 'r', label='Spectrum') #Plot the actual spectrum
plt.xlabel('Pixel Value')
plt.ylabel('Signal')
plt.legend(loc=2)
plt.show() 

residual = np.array(peaks) - np.array(centroids)
plt.plot(np.arange(len(residual)),residual,'bo')
plt.xlabel('Peak number (of those found)')
plt.ylabel('Residual [peak value - centroid value]')
plt.axhline(0,ls='-.')
plt.show()