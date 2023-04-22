from Wave import *

def test(fileName):
    wave = Wave(fileName)
    wave.read_wave()
    print(wave,end='')

if __name__ == '__main__':
    test('./sound-examples/ex14.wav')