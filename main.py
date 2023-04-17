from Wave import *

def test(fileName):
    with open(fileName,'rb') as f:
        wave = Wave()
        wave.read_wave(f)
        print(wave,end='')

if __name__ == '__main__':
    test('./sound-examples/ex11.wav')