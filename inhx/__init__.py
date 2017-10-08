class BaseIntelHexParser(object):
    """..."""

    address_cells = dict()
    address_divider = 1

    def __init__(self, filename):
        """..."""
        with open(filename, 'r') as file:
            for line in file.readlines():
                line = line[1:-1]
                data = {
                    'count': line[0:2],
                    'address': int(int(line[2:6], 16)/self.address_divider),
                    'type': line[6:8],
                    'bytes': line[8:-2],
                    'checksum': line[-2]
                }
                i=0;
                for b in range(0, int(data['count'], 16) * 2, 4):
                    low_byte = ''.join([
                        data['bytes'][b],
                        data['bytes'][b + 1]
                    ])
                    high_byte = ''.join([
                        data['bytes'][b + 2],
                        data['bytes'][b + 3]
                    ])

                    key = data['address']+i

                    self.address_cells[key] = (high_byte, low_byte)

                    i+=1

    def getData(self):
        return self.address_cells


class Inhx8(BaseIntelHexParser):
    address_divider = 2
