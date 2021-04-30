from chunks.jpeg_chunk import Chunk

"""
OPIS TODO!!!
"""

class EXIF_chunk(Chunk):



    """
    OPIS TODO!!!
    """

    def get_info(self, binary_table):
        
        i = 0
        while i < len(binary_table) -1:
            if binary_table[i] == 0x01:

                next_byte = binary_table[i+1]
                if next_byte == 0x00:

                    print(binary_table[i+2:i+8])
            i += 1

    ############################################################################################

    """
    Opis TODO!!!
    """

    def print_info(self):
        pass