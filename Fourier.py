import matplotlib.pyplot as plt
import librosa, librosa.display
import numpy as np

class Fourier():
    def __init__(self, fileName: str):
        try:
            self.signal, self.sr = librosa.load(fileName)
        except IOError as e:
            raise e

    def plot_magnitude_spectrum(self,title, f_ratio=1):
        X = np.fft.fft(self.signal)
        X_mag = np.absolute(X)
        
        plt.figure(figsize=(18, 5))
        
        f = np.linspace(0, self.sr, len(X_mag))
        f_bins = int(len(X_mag) * f_ratio)  
        
        plt.plot(f[:f_bins], X_mag[:f_bins])
        plt.xlabel('Frequency (Hz)')
        plt.title(title)
        plt.savefig("mygraph.png")