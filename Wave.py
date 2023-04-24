from Field import *
from Chunk import *
import copy
import os

chunks_ = [ TheRIFFChunk(), # mandatory chunk
            TheFmtChunk(),
            TheCueChunk(),
            TheFactChunk(),
            TheDataChunk(), # mandatory chunk
            TheListChunk(),
            TheInstrumentChunk(),
            TheSampleChunk() ]

class Wave():
    def __init__(self, fileName: str):

        try:
            self.file = open(fileName, 'rb')
        except IOError as e:
            raise e
        
        self.chunks = []

    # method to find and read all potential chunks in a file
    def read_wave(self):
        for chunk in chunks_.copy():
            try:
                positions = chunk.find_chunk(self.file)
                for pos in positions:
                    self.file.seek(pos)
                    chunk.read_chunk(self.file)
                    self.chunks.append(copy.deepcopy(chunk))
            except Exception as e:
                pass
                #print(e)

    def assert_wave(self):
        for chunk in self.chunks.copy():
            try:
                chunk.assert_chunk()
            except Exception as e:
                self.chunks.remove(chunk)
                #print(e)

    def clear_metadata(self):

        originalFileName = f'{self.file.name}'
        newFileNameBase = os.path.splitext(originalFileName)[0] # ./sound-examples/ex1

        newFileName_noMeta = f'{newFileNameBase}_noMeta.wav' # ./sound-examples/ex1_noMeta.wav

        file_noMeta = open(newFileName_noMeta, 'wb')

        for chunk in self.chunks:
            if not isinstance(chunk,TheListChunk):
                chunk.write_chunk(file_noMeta)

    def __str__(self):
        s=''
        for chunk in self.chunks:
            s = s + str(chunk)
        return s