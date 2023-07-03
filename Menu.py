from Wave import *
from Fourier import *
import sys

class Menu():
    def __init__(self):
        try:
            assert len(sys.argv) == 2
            self.pathToFile = sys.argv[1]
        except IOError as e:
            raise e
        
        self.wave = Wave(self.pathToFile)
        self.wave.read_wave()
        self.f1 = Fourier(self.pathToFile)
        
    def menu_loop(self):
        while True:
            print('Program menu')
            print('  (1) Display file chunks')
            print('  (2) Clear metadata of file')
            print('  (3) Create Fourier Transform')
            print('  (4) Encrypt file ecb')
            print('  (5) Decrypt file ecb')
            print('  (6) Encrypt file cbc')
            print('  (7) Decrypt file cbc')
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
                print(self.wave,end='')
            elif option == 2:
                self.wave.create_clean_copy()
                print('Your no metadata file has been created; now still operating on the original file')
            elif option == 3:
                self.f1.plot_fourier()
                print('File with fft plots has been created in project\'s directory')
            elif option == 4:
                self.wave.create_encrypted_copy('ecb')
                print('File has been encrypted using ecb method')
            elif option == 5:
                self.wave.create_decrypted_copy('ecb')
                print('File has been decrypted using ecb method')
            elif option == 6:
                self.wave.create_encrypted_copy('cbc')
                print('File has been encrypted using cbc method')
            elif option == 7:
                self.wave.create_decrypted_copy('cbc')
                print('File has been decrypted using cbc method only if you typed correct password')
            elif option == 0:
                break
            else:
                print('Option doesn\'t exist')