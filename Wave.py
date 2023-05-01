from Field import *
from Chunk import *
import copy
import os

class Wave():

    POSSIBLE_CHUNKS = [ TheRIFFChunk(), # mandatory chunk
                         TheFormatChunk(), # mandatory chunk
                         TheCueChunk(),
                         TheFactChunk(),
                         TheDataChunk(), # mandatory chunk
                         TheListChunk(),
                         TheInstrumentChunk(),
                         TheSampleChunk() ]

    def __init__(self, fileName: str):
        try:
            self.file = open(fileName, 'rb')
        except IOError as e:
            raise e
        
        self.chunks = []

    # method to find and read all potential chunks in a file
    def read_wave(self):
        for chunk in self.POSSIBLE_CHUNKS.copy():
            self.file.seek(0)
            try:
                positions = chunk.find_chunk(self.file)
                for pos in positions:
                    self.file.seek(pos)
                    chunk.read_chunk(self.file)
                    self.chunks.append(copy.deepcopy(chunk))
            except Exception as e:
                pass
                #print(e)

    def create_clean_copy(self):

        originalFileName = f'{self.file.name}'
        newFileNameBase = os.path.splitext(originalFileName)[0] # ./sound-examples/ex1

        newFileName_noMeta = f'{newFileNameBase}_noMeta.wav' # ./sound-examples/ex1_noMeta.wav

        file_noMeta = open(newFileName_noMeta, 'wb')

        for chunk in self.chunks:
            if isinstance(chunk,TheRIFFChunk) or isinstance(chunk,TheFormatChunk) or isinstance(chunk,TheDataChunk):
                chunk.write_chunk(file_noMeta)

    def __str__(self):
        s=''
        for chunk in self.chunks:
            s = s + str(chunk)
        return s