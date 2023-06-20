from Wave import *
from Fourier import *
import sys

def menu():

    try:
        assert len(sys.argv) == 2
        pathToFile = sys.argv[1]
    except IOError as e:
        raise e

    wave = Wave(pathToFile)
    wave.read_wave()

    f1 = Fourier(pathToFile)

    while True:
        print('Program menu')
        print('  (1) Display file chunks')
        print('  (2) Clear metadata of file')
        print('  (3) Create Fourier Transform')
        print('  (0) Exit the program')

        try:
            option = int(input('Enter your option here: '))
        except KeyboardInterrupt:
            print()
            break
        except:
            print('Wrong input. Please enter a number')
            continue

        if option == 1:
            print(wave,end='')
        elif option == 2:
            wave.create_clean_copy()
            print('Your no metadata file has been created; now still operating on the original file')
        elif option == 3:
            f1.plot_fourier()
            print('File with fft plots has been created in project\'s directory')     
        elif option == 0:
            break
        else:
            print('Option doesn\'t exist')