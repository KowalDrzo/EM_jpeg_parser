from chunks.jpeg_chunk import Chunk

"""
OPIS TODO!!!
"""

class SOS_chunk(Chunk):

    components_nb = 0
    components = []

    spectral = [int] * 2
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

        self.spectral[0] = binary_table[self.components_nb * 2 + 3]
        self.spectral[1] = binary_table[self.components_nb * 2 + 4]
        self.approx = binary_table[self.components_nb * 2 + 5]

    ############################################################################################

    """
    Opis TODO!!!
    """

    def print_info(self):
        
        print("\nInformacje o chunku Start of Scan:\n")
        
        for i in range(0, self.components_nb):
            
            component = self.components[i]
            print("Komponent nr " + str(i) + ":")
            print("Selektor: " + str(component[0]))
            print("Składowa zmienna: " + str(component[1] & 0x0f) + " Składowa stała: " + str(component[1] >> 4))
        
        print("Wybór spektralny: " + str(self.spectral))
        print("Przybliżenie kwantyzacji: " + str(self.approx))