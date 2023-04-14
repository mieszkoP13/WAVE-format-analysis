from abc import abstractmethod, ABC

class bcolors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    PRPLE = '\033[35m'
    YELLW = '\033[33m'
    WHITE = '\033[97m'
    ENDC = '\033[0m'

class Field(ABC):
    def __init__(self, name:str, size:int, offset:int, encoding:str, endian:str, isDataCrucial:bool):
        self.name = name
        self.size = size
        self.offset = offset
        self.encoding = encoding
        self.endian = endian

        # Informs if data of this field is vital to the analysis; if not, it shall not be displayable
        self.isDataCrucial = isDataCrucial
        self.data = None

    def __str__(self):
        return f'{bcolors.BLUE}Name: {self.name}{bcolors.ENDC}, '\
               f'{bcolors.YELLW}Size: {self.size}{bcolors.ENDC}, '\
               f'{bcolors.PRPLE}Data: { self.data if self.isDataCrucial else "..."}{bcolors.ENDC}, '\
               f'{bcolors.CYAN}Offset: {self.offset}{bcolors.ENDC}, '\
               f'{bcolors.GREEN}Encoding: {self.encoding}{bcolors.ENDC}, '\
               f'{bcolors.WHITE}Endian: {self.endian}{bcolors.ENDC}'
    
    @abstractmethod
    def read_field(self,file):
        pass


class TextField(Field):
    def __init__(self, name:str, size:int, offset:int, encoding:str, endian:str, isDataCrucial:bool):
        super().__init__(name, size, offset, encoding, endian, isDataCrucial)

    def read_field(self,file):
        self.data = file.read(self.size).decode(self.encoding)

class NumberField(Field):
    def __init__(self, name:str, size:int, offset:int, encoding:str, endian, isDataCrucial:bool):
        super().__init__(name, size, offset, encoding, endian, isDataCrucial)

    def read_field(self,file):
        self.data = int.from_bytes(file.read(self.size), self.endian)