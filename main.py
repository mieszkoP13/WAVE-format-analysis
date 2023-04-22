from Wave import *

def test(fileName):
    wave = Wave(fileName)
    wave.read_wave()
    wave.assert_wave()
    print(wave,end='')

if __name__ == '__main__':
    test('./sound-examples/ex18.wav')