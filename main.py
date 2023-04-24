from Wave import *
from Fourier import *

def test(fileName):
    wave = Wave(fileName)
    wave.read_wave()
    wave.assert_wave()
    wave.clear_metadata()
    print(wave,end='')

def test_fourier(fileName):
    f1 = Fourier(fileName)
    f1.plot_magnitude_spectrum('test',1)

if __name__ == '__main__':
    test('./sound-examples/ex1.wav')
    #test_fourier('./sound-examples/ex1.wav')

#### todo ####
# junk chunk
# pad chunk
# id3 chunk
# bext chunk
# cart chunk
# ds64 chunk