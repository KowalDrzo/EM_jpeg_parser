from chunks.jpeg_chunk import Chunk

"""
OPIS TODO!!!
"""

class ADH_chunk(Chunk):

    identifier = ""
    version = []
    units = 0
    density = []
    thumbnail = []

    """
    OPIS TODO!!!
    """

    def get_info(self, binary_table):
        
        for char in binary_table[2:6]:
            self.identifier += chr(char)

        self.version.append(binary_table[7])
        self.version.append(binary_table[8])

        self.units = binary_table[9]

        self.density.append((binary_table[10] << 8) | binary_table[11])
        self.density.append((binary_table[12] << 8) | binary_table[13])

        self.thumbnail.append(binary_table[14])
        self.thumbnail.append(binary_table[15])

    ############################################################################################

    """
    Opis TODO!!!
    """

    def print_info(self):
        
        print("\nInformacje o chunku Application default header:\n")
        print("Identyfikator: " + self.identifier)
        print("Wersja: " + str(self.version[0]) + "." + str(self.version[1]))
        print("Jednostki Dpi: " + str(self.units))
        print("Gęstość: " + str(self.density[0]) + "*" + str(self.density[1]))
        print("Miniatura: " + str(self.thumbnail[0]) + "*" + str(self.thumbnail[1]))