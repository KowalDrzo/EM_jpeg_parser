from chunks.jpeg_chunk import Chunk
from chunks.sof import SOF_chunk

"""
Klasa zajmująca się parsowaniem i przechowywaniem elementów odczytanych z chunku Exif.
"""

class EXIF_chunk(Chunk):

    identifier = ""
    
    jpeg_thumbnail = False
    thumbnail_sof = None

    ifd_offset = []
    ifd_components_nb = []

    camera_manufacturer = ""
    camera_model = ""
    camera_soft = ""

    original_date = ""
    copyrights = ""

    exposure_time = 0.0
    exposure_program = 0

    resX = 0
    resY = 0

    ############################################################################################

    """
    Metoda parsująca chunk i zapisująca dane wyczytane z niego.
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

        # Poszukiwania miniatury:
        i = 16
        while i < len(binary_table):
            
            if binary_table[i] == 0xff:

                next_byte = binary_table[i+1]

                if next_byte == 0xd8:
                    self.jpeg_thumbnail = True
            
                elif next_byte >= 0xc0 and next_byte <= 0xcf and next_byte != 0xc4 and next_byte != 0xc8 and next_byte != 0xcc:
                    
                    sof_len = (binary_table[i+2] << 8) | binary_table[i+3]

                    self.thumbnail_sof = SOF_chunk()
                    self.thumbnail_sof.get_info(binary_table[i+2:i+2 + sof_len], next_byte & 0x0f)
                    break

            i += 1

        # Szukanie innych markerów:
        i = 16
        while i < len(binary_table):

            if binary_table[i] == 0x01:

                next_byte = binary_table[i+1]
                
                if next_byte == 0x0f:
                    self.camera_manufacturer = self.ascii_read(binary_table[i+2:])

                elif next_byte == 0x10:
                    self.camera_model = self.ascii_read(binary_table[i+2:])

                elif next_byte == 0x31:
                    self.camera_soft = self.ascii_read(binary_table[i+2:])

                elif next_byte == 0x32:
                    self.original_date = self.ascii_read(binary_table[i+2:i+22])
                    print(self.original_date)

            elif binary_table[i] == 0x82:

                next_byte = binary_table[i+1]

                if next_byte == 0x98:
                    self.copyrights = self.ascii_read(binary_table[i+2:])

                elif next_byte == 0x9a:
                    self.exposure_time = self.link_bytes(binary_table[i+2:i+6]) / self.link_bytes(binary_table[i+6:i+10])

            elif binary_table[i] == 0x88 and binary_table[i+1] == 0x22 and self.exposure_program == 0:
                self.exposure_program = self.link_bytes(binary_table[i+2:i+4])

            elif binary_table[i] == 0xa0:

                next_byte = binary_table[i+1]

                if next_byte == 0x02:
                    self.resY = self.link_bytes(binary_table[i+2:i+6])

                elif next_byte == 0x03:
                    self.resX = self.link_bytes(binary_table[i+2:i+6])

            i += 1

        



    ############################################################################################

    """
    Metoda zajmująca się łączeniem kilku podanych bajtów w jedną liczbę z zachowaniem trybu Low lub Big endian.
    """

    def link_bytes(self, binary_subtable: list) -> int:

        result = 0

        if self.low_endian:
            binary_subtable.reverse()

        for byte in binary_subtable:
            result << 8
            result |= byte

        return result

    ############################################################################################

    """
    Metoda czytająca napis ascii aż do napotkania wartości 0.
    """

    def ascii_read(self, binary_subtable: list) -> str:

        result = ""

        for char in binary_subtable:
            
            result += chr(char)
            if char == 0:
                break

        return result

    ############################################################################################

    """
    Rekurencyjna metoda szukająca Image File Directories - offsetów informacji o zdjęciu / miniaturze itp.
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
    Metoda wyświetlająca odczytane wcześniej dane.
    """

    def print_info(self):
        
        print("\nInformacje o chunku Exif:\n")
        print("Identyfikator: " + self.identifier)

        if self.low_endian:
            print("Tryb łączenia bajtów: Low endian")
        else:
            print("Tryb łączenia bajtów: Big endian")

        print("Ilość elementów ifd: " + str(len(self.ifd_components_nb)))

        for i in range(0, len(self.ifd_components_nb)):
            print("Element nr " + str(i) + ":")
            print("offset: " + str(self.ifd_offset[i]))
            print("ilość wpisów: " + str(self.ifd_components_nb[i]))

        if self.jpeg_thumbnail:
            
            print("Exif zawienia miniaturę w formacie Jpeg")
            print("Dane miniatury:")
            self.thumbnail_sof.print_info()
            print("")

        else:
            print("Exif nie zawiera miniatury")

        if self.camera_manufacturer:
            print("Producent aparatu: " + self.camera_manufacturer)

        if self.camera_model:
            print("Model aparatu:" + self.camera_model)

        if self.camera_soft:
            print("Oprogramowanie aparatu:" + self.camera_soft)

        if self.original_date:
            print("Oryginalna data obrazu: " + self.original_date)

        if self.copyrights:
            print("Prawa autorskie: " + self.copyrights)

        if self.exposure_time != 0.0:
            print("Czas ekspozycji: " + str(self.exposure_time))

        if self.exposure_program > 0:
            result = ""

            if self.exposure_program == 1:
                result = "manualny"
            elif self.exposure_program == 2:
                result = "normalny"
            elif self.exposure_program == 3:
                result = "priorytet przysłony"
            elif self.exposure_program == 4:
                result = "priorytet migawki"
            elif self.exposure_program == 5:
                result = "długi czas naświetlania"
            elif self.exposure_program == 6:
                result = "krótki czas naświetlania"
            elif self.exposure_program == 7:
                result = "portret"
            elif self.exposure_program == 8:
                result = "krajobraz"
            else:
                result = "inny"


            print("Program ekspozycji: " + result)

        if self.resY != 0 and self.resX != 0:
            print("Rozdzielczość: " + str(self.resY) + ":" + str(self.resX))