import matplotlib.pyplot as plt
import librosa, librosa.display
import numpy as np

class Fourier():
    def __init__(self, fileName: str):
        try:
            self.signal, self.sr = librosa.load(fileName)
        except IOError as e:
            raise e

    def plot_magnitude_spectrum(self, f_ratio=1):
        spectrum = np.fft.fft(self.signal)
        magnitude = np.absolute(spectrum)
        phase = np.angle(spectrum)
        
        plt.figure(figsize=(12, 10))
        
        mag_linspace = np.linspace(0, self.sr, len(magnitude))
        mag_linspace_bins = int(len(mag_linspace) * f_ratio)

        phs_linspace = np.linspace(0, self.sr, len(phase))
        phs_linspace_bins = int(len(phs_linspace) * f_ratio) 
        
        plt.subplot(211)
        plt.plot(mag_linspace[:mag_linspace_bins], magnitude[:mag_linspace_bins])
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.savefig("mygraph.png")

        plt.subplot(212)
        plt.plot(phs_linspace[:phs_linspace_bins], phase[:phs_linspace_bins])
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Phase')
        plt.savefig("mygraph.png")