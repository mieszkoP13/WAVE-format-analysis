from Field import *
from Chunk import *

class Wave():
    chunks = [ TheRIFFChunk(), # mandatory chunk
               TheFmtChunk(),
               TheDataChunk(), # mandatory chunk
               TheListChunk() ]

    def read_wave(self,file):
        for chunk in self.chunks:
            chunk.read_chunk(file)

            if chunk.fields[0].data != chunk.chunkAssertID:
                self.chunks.remove(chunk)

    def __str__(self):
        s=''
        for chunk in self.chunks:
            s = s + str(chunk)
        return s