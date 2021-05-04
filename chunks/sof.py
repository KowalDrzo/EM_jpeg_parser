from chunks.jpeg_chunk import Chunk

"""
Klasa zajmująca się parsowaniem i przechowywaniem elementów odczytanych z chunku SOF.
"""

class SOF_chunk(Chunk):

    sof_nb = 0

    precision = 0
    height = 0
    width = 0

    components_nb = 0
    components = []

    """
    Metoda parsująca chunk i zapisująca dane wyczytane z niego.
    """

    def get_info(self, binary_table, number):

        self.sof_nb = number

        self.precision = binary_table[2]
        self.height = (binary_table[3] << 8) | binary_table[4]
        self.width = (binary_table[5] << 8) | binary_table[6]
        self.components_nb = binary_table[7]

        for i in range(0, self.components_nb):
            
            id = binary_table[8+i*3]
            factor = binary_table[9+i*3]
            qt_nb = binary_table[10+i*3]
            self.components.append([id, factor, qt_nb])

    ############################################################################################

    """
    Metoda wyświetlająca odczytane wcześniej dane.
    """

    def print_info(self):

        print("\nInformacje o chunku Start of Frame (typ " + str(self.sof_nb) + "):\n")
        print("Głębia bitowa: "     + str(self.precision)   + " bit")
        print("Wysokość obrazu: "   + str(self.height)      + " pix")
        print("szerokość obrazu: "  + str(self.width)       + " pix")
        print("Ilość komponentów: " + str(self.components_nb))

        for i in range(0, self.components_nb):
            component = self.components[i]
            print("Komponent nr " + str(i) + ":")

            if component[0] == 1:
                print("Luminancja")
            elif component[0] == 2:
                print("Chrominancja Cb")
            elif component[0] == 3:
                print("Chrominancja Cr")
            else:
                print("Inny rodzaj komponentu")
            
            print("Mnożnik próbkowania: Pionowo: " + str(component[1] & 0x0f) + " Poziomo: " + str(component[1] >> 4))
            print("Nr tabeli kwantyzacji komponentu: " + str(component[2]))