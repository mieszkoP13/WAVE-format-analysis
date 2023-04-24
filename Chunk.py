from abc import abstractmethod, ABC
from typing import Type
from Field import *

class Chunk(ABC):
    def __init__(self, chunkName: str, chunkAssertID: str, fields:Type[Field]=None):
        if fields is None:
            self.fields = []

        self.chunkName = chunkName
        self.chunkAssertID = chunkAssertID
        self.fields = fields

    def find_chunk(self,file):
        fileTxt = file.read()
        # finding a all the positions of a chunk candidates by its ID
        positions = [i for i in range(len(fileTxt)) if fileTxt.startswith(f'{self.chunkAssertID}'.encode(), i)]

        # if no position was found
        if not positions:
            file.seek(0)
            raise Exception("chunk not found")
        
        return positions

    @abstractmethod
    def read_chunk(self,file):
        pass

    @abstractmethod
    def assert_chunk(self,file):
        pass

    def __str__(self):
        s=f'{self.chunkName}\n'
        for field in self.fields:
            s = s + str(field) + '\n'
        return s
    
    def fieldCount(self):
        return len(self.fields)


class TheRIFFChunk(Chunk):

    def __init__(self):
        super().__init__('The RIFF Chunk','RIFF',[TextField('RIFF Chunk ID',4,'UTF-8','big',True),
                        NumberField('RIFF Chunk Size',4,'UTF-32','little',True),
                        TextField('RIFF type ID',4,'UTF-8','big',True)])
        
    def read_chunk(self,file):
        for field in self.fields:
            field.read_field(file)
        file.seek(0)
    
    def assert_chunk(self):
        assert self.fields[0].data == 'RIFF', f'Invalid {self.fields[0].name}'
        assert self.fields[1].data > 0, f'Invalid {self.fields[1].name}'
        assert self.fields[2].data == 'WAVE', f'Invalid {self.fields[2].name}'


class TheFmtChunk(Chunk):

    def __init__(self):
        super().__init__('The Fmt Chunk','fmt ', [TextField('Fmt Chunk ID',4,'UTF-8','big',True),
        NumberField('Fmt Chunk Size',4,'UTF-8','little',True),
        NumberField('Audio Format',2,'UTF-8','little',True),
        NumberField('Number of Channels',2,'UTF-8','little',True),
        NumberField('Sample Rate',4,'UTF-32','little',True),
        NumberField('Byte Rate',4,'UTF-32','little',True),
        NumberField('Block Align',2,'UTF-8','little',True),
        NumberField('Bits Per Sample',2,'UTF-8','little',True)])

    def read_chunk(self,file):
        for field in self.fields:
            field.read_field(file)
        file.seek(0)

    def assert_chunk(self):
        assert self.fields[0].data == 'fmt ', f'Invalid {self.fields[0].name}'
        assert self.fields[1].data > 0, f'Invalid {self.fields[1].name}'
        assert self.fields[2].data > 0, f'Invalid {self.fields[2].name}'
        assert self.fields[3].data > 0, f'Invalid {self.fields[3].name}'
        assert self.fields[4].data > 0, f'Invalid {self.fields[4].name}'
        assert self.fields[5].data > 0, f'Invalid {self.fields[5].name}'
        assert self.fields[6].data > 0, f'Invalid {self.fields[6].name}'
        assert self.fields[7].data > 0, f'Invalid {self.fields[7].name}'
        

class TheDataChunk(Chunk):

    def __init__(self):
        super().__init__('The Data Chunk','data',[TextField('Data Chunk ID',4,'UTF-8','big',True),
        NumberField('Data Chunk Size',4,'UTF-32','little',True),
        TextField('Data Chunk Data',None,'ISO-8859-1','little',False)])

    def read_chunk(self,file):
        self.fields[0].read_field(file)
        self.fields[1].read_field(file)
        self.fields[2].size = self.fields[1].data
        self.fields[2].read_field(file)
        file.seek(0)

    def assert_chunk(self):
        assert self.fields[0].data == 'data', f'Invalid {self.fields[0].name}'
        assert self.fields[1].data > 0, f'Invalid {self.fields[1].name}'
  
class TheFactChunk(Chunk):

    def __init__(self):
        super().__init__('The Fact Chunk','fact',[TextField('Fact Chunk ID',4,'UTF-8','big',True),
        NumberField('Fact Chunk Size',4,'UTF-32','little',True),
        TextField('Fact Chunk Data',None,'ISO-8859-1','little',True)])

    def read_chunk(self,file):
        self.fields[0].read_field(file)
        self.fields[1].read_field(file)
        self.fields[2].size = self.fields[1].data
        self.fields[2].read_field(file)
        file.seek(0)

    def assert_chunk(self):
        assert self.fields[0].data == 'fact', f'Invalid {self.fields[0].name}'
        assert self.fields[1].data > 0, f'Invalid {self.fields[1].name}'

class TheListChunk(Chunk):

    LIST_CHUNK_INFO_ID = [ 'IARL','IART','ICMS',
                           'ICMT','ICOP','ICRD',
                           'ICRP','IDIM','IDPI',
                           'IENG','IGNR','IKEY',
                           'ILGT','IMED','INAM',
                           'IPLT','IPRD','ISBJ',
                           'ISFT','ISRC','ISRF',
                           'ITCH', 'ITRK' ]

    # this init is incomplete and only contains 3 'preamble' fields which will or will not be followed by list of other subchunks
    def __init__(self):
        super().__init__('The List Chunk','LIST',[TextField('List Chunk ID',4,'UTF-8','big',True),
        NumberField('List Chunk Size',4,'UTF-32','little',True),
        TextField('List Type ID',4,'UTF-8','big',True)])

    def read_chunk(self,file):
        self.fields[0].read_field(file)
        self.fields[1].read_field(file)
        self.fields[2].read_field(file)

        if self.fields[2].data == 'INFO':
            while(1):
                infoID = TextField('List Chunk ID',4,'UTF-8','big',True)
                infoID.read_field(file)
                
                if infoID.data not in self.LIST_CHUNK_INFO_ID:
                    break

                size = NumberField('List Chunk Size',4,'UTF-32','little',True)
                size.read_field(file)
                text = TextField('List Type ID',size.data,'UTF-8','big',True)
                text.read_field(file)

                self.fields.append(infoID)
                self.fields.append(size)
                self.fields.append(text)
        file.seek(0)
    
    def assert_chunk(self):
        assert self.fields[0].data == 'LIST', f'Invalid {self.fields[0].name}'
        assert self.fields[1].data > 0, f'Invalid {self.fields[1].name}'

class TheCueChunk(Chunk):

    def __init__(self):
        super().__init__('The Cue Chunk','cue ',[TextField('Fact Chunk ID',4,'UTF-8','big',True),
        NumberField('Cue Chunk Size',4,'UTF-32','little',True),
        NumberField('Number of Cue Points',4,'UTF-32','little',True)])

    def read_chunk(self,file):
        self.fields[0].read_field(file)
        self.fields[1].read_field(file)
        self.fields[2].read_field(file)

        for _ in range(self.fields[2].data):
            id = TextField('Cue Point ID',4,'UTF-8','big',True)
            id.read_field(file)
            pos = NumberField('Cue Point Position',4,'UTF-32','little',True)
            pos.read_field(file)
            dataChunkID = TextField('Cue Point Data Chunk ID',4,'UTF-8','big',True)
            dataChunkID.read_field(file)
            chunkStart = NumberField('Chunk Start',4,'UTF-32','little',True)
            chunkStart.read_field(file)
            blockStart = NumberField('Block Start',4,'UTF-32','little',True)
            blockStart.read_field(file)
            sampleStart = NumberField('Sample Start',4,'UTF-32','little',True)
            sampleStart.read_field(file)

            self.fields.append(id)
            self.fields.append(pos)
            self.fields.append(dataChunkID)
            self.fields.append(chunkStart)
            self.fields.append(blockStart)
            self.fields.append(sampleStart)
        file.seek(0)

    def assert_chunk(self):
        pass
        #assert self.fields[0].data == 'fact', f'Invalid {self.fields[0].name}'
        #assert self.fields[1].data > 0, f'Invalid {self.fields[1].name}'

class TheInstrumentChunk(Chunk):

    def __init__(self):
        super().__init__('The Instrument Chunk','inst', [TextField('Instrument Chunk ID',4,'UTF-8','big',True),
        NumberField('Instrument Chunk Size',4,'UTF-8','little',True),
        NumberField('Uunshifted note',1,'UTF-8','little',True),
        NumberField('Fine tuning',1,'UTF-8','little',True),
        NumberField('Gain',1,'UTF-8','little',True),
        NumberField('Low note',1,'UTF-8','little',True),
        NumberField('High note',1,'UTF-8','little',True),
        NumberField('Low velocity',1,'UTF-8','little',True),
        NumberField('Low velocity',1,'UTF-8','little',True)])

    def read_chunk(self,file):
        for field in self.fields:
            field.read_field(file)
        file.seek(0)

    def assert_chunk(self):
        assert self.fields[0].data == 'inst', f'Invalid {self.fields[0].name}'
        assert self.fields[1].data >= 0, f'Invalid {self.fields[1].name}'
        assert self.fields[2].data >= 0, f'Invalid {self.fields[2].name}'
        assert self.fields[3].data >= 0, f'Invalid {self.fields[3].name}'
        assert self.fields[4].data >= 0, f'Invalid {self.fields[4].name}'
        assert self.fields[5].data >= 0, f'Invalid {self.fields[5].name}'
        assert self.fields[6].data >= 0, f'Invalid {self.fields[6].name}'
        assert self.fields[7].data >= 0, f'Invalid {self.fields[7].name}'
        ##############

class TheSampleChunk(Chunk):

    def __init__(self):
        super().__init__('The Sample Chunk','smpl',[TextField('Sample Chunk ID',4,'UTF-8','big',True),
        NumberField('Sample Chunk Size',4,'UTF-32','little',True),
        NumberField('Manufacturer',4,'UTF-32','little',True),
        NumberField('Product',4,'UTF-32','little',True),
        NumberField('Sample period',4,'UTF-32','little',True),
        NumberField('MIDI unity note',4,'UTF-32','little',True),
        NumberField('MIDI pitch fraction',4,'UTF-32','little',True),
        NumberField('SMPTE format',4,'UTF-32','little',True),
        NumberField('SMPTE offset',4,'UTF-32','little',True),
        NumberField('Number of sample loops',4,'UTF-32','little',True),
        NumberField('Sample data',4,'UTF-32','little',True)])

    def read_chunk(self,file):
        for field in self.fields:
            field.read_field(file)

        for _ in range(self.fields[9].data):
            id_ = TextField('Sample loop ID',4,'UTF-8','big',True)
            id_.read_field(file)
            type_ = NumberField('Sample loop Type',4,'UTF-32','little',True)
            type_.read_field(file)
            start_ = NumberField('Sample loop Start',4,'UTF-32','little',True)
            start_.read_field(file)
            end_ = NumberField('Sample loop End',4,'UTF-32','little',True)
            end_.read_field(file)
            fraction_ = NumberField('Sample loop Fraction',4,'UTF-32','little',True)
            fraction_.read_field(file)
            numberOfTimesToPlayTheLoop_ = NumberField('Number of times to play the loop',4,'UTF-32','little',True)
            numberOfTimesToPlayTheLoop_ .read_field(file)
            
            self.fields.append(id_)
            self.fields.append(type_)
            self.fields.append(start_)
            self.fields.append(end_)
            self.fields.append(fraction_)
            self.fields.append(numberOfTimesToPlayTheLoop_)
        file.seek(0)

    def assert_chunk(self):
        pass
        #assert self.fields[0].data == 'fact', f'Invalid {self.fields[0].name}'
        #assert self.fields[1].data > 0, f'Invalid {self.fields[1].name}'