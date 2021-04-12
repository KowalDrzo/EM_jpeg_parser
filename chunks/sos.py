from chunks.jpeg_chunk import Chunk

"""
OPIS TODO!!!
"""

class SOS_chunk(Chunk):

    components_nb = 0
    components = []

    spectral = []
    approx = 0

    """
    OPIS TODO!!!
    """

    def get_info(self, binary_table):
        
        self.components_nb = binary_table[2]

        for i in range(0, self.components_nb):
            
            selector = binary_table[3+i*2]
            dc_ac = binary_table[4+i*2]
            self.components.append([selector, dc_ac])

        self.spectral.append(binary_table[self.components_nb * 2 + 3])
        self.spectral.append(binary_table[self.components_nb * 2 + 4])
        self.approx = binary_table[self.components_nb * 2 + 5]

    ############################################################################################

    """
    Opis TODO!!!
    """

    def print_info(self):
        
        print("\nInformacje o chunku Start of Scan:\n")