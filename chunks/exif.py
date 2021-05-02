from chunks.jpeg_chunk import Chunk

"""
OPIS TODO!!!
"""

class EXIF_chunk(Chunk):

    identifier = ""
    low_endian = False
    
    ifd_offset = []
    ifd_components_nb = []

    ############################################################################################

    """
    OPIS TODO!!!
    """

    def parse_exif(self, binary_table: list):
        
        for char in binary_table[2:6]:
            self.identifier += chr(char)

        # Czytanie nagłówka TIFF:
        if binary_table[8:10] == [0x49, 0x49]:
            self.low_endian = True
            
        elif binary_table[8:10] == [0x4d, 0x4d]:
            self.low_endian = False

        if self.link_bytes(binary_table[10:12]) != 42:
            print("Blad czytania nagłówka TIFF!")
            raise ValueError        

        self.read_offset_ifd(binary_table, 12)

    ############################################################################################

    """
    Opis TODO!!!
    """

    def link_bytes(self, binary_subtable: list) -> int:

        result = 0

        if self.low_endian:
            binary_subtable.reverse()

        for byte in binary_subtable:
            result |= byte
            result << 8

        result >> 8

        return result

    ############################################################################################

    """
    Opis TODO!!!
    """

    def read_offset_ifd(self, binary_table: list, beg) -> int:

        self.ifd_offset.append(self.link_bytes(binary_table[beg:beg+4]))
        self.ifd_components_nb.append(self.link_bytes(binary_table  [8+self.ifd_offset[-1]  :   8+self.ifd_offset[-1]+2]    ))
        
        link_offset = self.ifd_offset[-1]+12*self.ifd_components_nb[-1]

        if binary_table[8+link_offset:8+link_offset+4] == [0, 0, 0, 0]:
            return

        self.read_offset_ifd(binary_table, link_offset)

    ############################################################################################

    """
    Opis TODO!!!
    """

    def print_info(self):
        
        print("\nInformacje o chunku Exif:\n")
        print("Identyfikator: " + self.identifier)
        print("Ilość elementów ifd: " + str(len(self.ifd_components_nb)))

        for i in range(0, len(self.ifd_components_nb)):
            print("Element nr " + str(i) + ":")
            print("offset: " + str(self.ifd_offset[i]))
            print("ilość wpisów: " + str(self.ifd_components_nb[i]))