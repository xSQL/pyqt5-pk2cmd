import struct


class BinaryReader(object):
    '''Port some C# binary reader methods'''
    
    def __init__(self, filename):
        """..."""
        self.file = open(filename, 'rb')
    
    def __enter__(self):
        return self
        
    def __exit__(self, *args):
        self.file.close()

    def _byte2int(self, b):
        """Return int value of byte"""
        data = struct.unpack('<B', b)
        return data[0]

    def read_string(self):
        """Return string decoded by 7-bit method"""
        stringLength = 0
        stringLengthParsed = False
        step = 0
        while not stringLengthParsed:
            part = self._byte2int(self.read_byte())
            stringLengthParsed = ((part >> 7) == 0)
            partCutter = part & 127
            toAdd = partCutter << (step*7)
            stringLength += toAdd
            step+=1
        return self.file.read(stringLength).decode('utf-8')

    def read_uint32(self):
        """Return 4-bytes unsigned integer"""
        b = self.file.read(4)
        data = struct.unpack('<I', b)
        return data[0]

    def read_uint16(self):
        """Return 2-bytes unsigned integer"""
        b = self.file.read(2)
        data = struct.unpack('<H', b)
        return data[0]

    def read_int32(self):
        """Return 4-bytes signed integer"""
        b = self.file.read(4)
        data = struct.unpack('<i', b)
        return data[0]

    def read_int16(self):
        """Return 2-bytes signed integer"""
        b = self.file.read(2)
        data = struct.unpack('<h', b)
        return data[0]

    def read_byte(self):
        """Return 1 byte"""
        return self.file.read(1)

    def read_boolean(self):
        """Return boolean value"""
        b = self.read_byte()
        data = struct.unpack('=?', b)
        return data[0]

    def read_single(self):
        """Return floating point value encoded by 4-bytes"""
        b = self.file.read(4)
        data = struct.unpack('<f', b)
        return data[0]


