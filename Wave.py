from Field import *
from Chunk import *

class TheRIFFChunk(Chunk):
    def __init__(self):
        super().__init__([TextField('Chunk ID',4,0,'UTF-8','big',True),
                        NumberField('Chunk Size',4,4,'UTF-32','little',True),
                        TextField('Format',4,8,'UTF-8','big',True)])
        
    def read_chunk(self,file):
        for field in self.fields:
            field.read_field(file)


class TheFmtChunk(Chunk):
    def __init__(self):
        super().__init__([TextField('Subchunk1 ID',4,12,'UTF-8','big',True),
        NumberField('Subchunk1 Size',4,16,'UTF-8','little',True),
        NumberField('Audio Format',2,20,'UTF-8','little',True),
        NumberField('Number of Channels',2,22,'UTF-8','little',True),
        NumberField('Sample Rate',4,24,'UTF-32','little',True),
        NumberField('Byte Rate',4,28,'UTF-32','little',True),
        NumberField('Block Align',2,32,'UTF-8','little',True),
        NumberField('Bits Per Sample',2,34,'UTF-8','little',True)])

    def read_chunk(self,file):
        for field in self.fields:
            field.read_field(file)
        

class TheDataChunk(Chunk):
    def __init__(self):
        super().__init__([TextField('Subchunk2 ID',4,36,'UTF-8','big',True),
        NumberField('Subchunk2 Size',4,40,'UTF-32','little',True),
        TextField('Data',None,44,'ISO-8859-1','little',False)])

    def read_chunk(self,file):
        self.fields[0].read_field(file)
        self.fields[1].read_field(file)
        self.fields[2].size = self.fields[1].data
        self.fields[2].read_field(file)
        
class TheListChunk(Chunk):

    LIST_CHUNK_INFO_ID = [ 'IARL','IART','ICMS',
                           'ICMT','ICOP','ICRD',
                           'ICRP','IDIM','IDPI',
                           'IENG','IGNR','IKEY',
                           'ILGT','IMED','INAM',
                           'IPLT','IPRD','ISBJ',
                           'ISFT','ISRC','ISRF','ITCH' ]

    # this init is incomplete and only contains 3 'preamble' fields which will or will not be followed by list of other subchunks containing some data
    def __init__(self):
        super().__init__([TextField('List Chunk ID',4,336,'UTF-8','big',True),
        NumberField('List Chunk Size',4,440,'UTF-32','little',True),
        TextField('List Type ID',4,3336,'UTF-8','big',True)])

    def read_chunk(self,file):
        self.fields[0].read_field(file)
        self.fields[1].read_field(file)
        self.fields[2].read_field(file)

        while(self.is_infoID_valid(file)):
            infoID = TextField('List Chunk ID',4,336,'UTF-8','big',True)
            infoID.read_field(file)
            size = NumberField('List Chunk Size',4,440,'UTF-32','little',True)
            size.read_field(file)
            text = TextField('List Type ID',size.data,3336,'UTF-8','big',True)
            text.read_field(file)
            self.fields.append(infoID)
            self.fields.append(size)
            self.fields.append(text)
                
    def is_infoID_valid(self,file):
        testID = TextField('test ID',4,1111,'UTF-8','big',True)
        testID.read_field(file)
        file.seek(file.tell()-4)

        if testID.data in self.LIST_CHUNK_INFO_ID:
            return True
        return False

class Wave():
    chunks = [ TheRIFFChunk(), # mandatory chunk
               TheFmtChunk(),
               TheDataChunk(), # mandatory chunk
               TheListChunk() ]

    def read_wave(self,file):
        for chunk in self.chunks:
            chunk.read_chunk(file)

    def __str__(self):
        s=''
        for chunk in self.chunks:
            s = s + str(chunk)
        return s