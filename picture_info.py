
class PictureInfo:

    file = None
    binary_image = []

    ############################################################################################

    def __init__(self, file_name):
        self.file = open(file_name, "rb")

    def __del__(self):
        self.file.close()

    ############################################################################################

    def read_chunk_nl(self) -> int:
        return int.from_bytes(self.file.read(2), "big")

    ############################################################################################

    def check_soi(self):

        int_byte = self.read_chunk_nl()

        if int_byte != 0xffd8:
            
            print("Niepoprawny JPEG!")
            raise IOError

    ############################################################################################

    def read_adh(self):

        chunk_len = self.read_chunk_nl() -2
        test = self.file.read(chunk_len)

        print("Wykryto chunk ADH")

    ############################################################################################

    def read_qt(self):

        chunk_len = self.read_chunk_nl() -2
        test = self.file.read(chunk_len)

        print("Wykryto chunk QT")

    ############################################################################################

    def read_sof(self):

        chunk_len = self.read_chunk_nl() -2
        test = self.file.read(chunk_len)

        print("Wykryto chunk SOF")

    ############################################################################################

    def read_dht(self):

        chunk_len = self.read_chunk_nl() -2
        test = self.file.read(chunk_len)

        print("Wykryto chunk DHT")
    
    ############################################################################################

    def read_image(self):

        chunk_len = self.read_chunk_nl() -2
        test = self.file.read(chunk_len)

        while True:
            test = int.from_bytes(self.file.read(1), "big")
            if test != 0xff:
                self.binary_image.append(test)
            else:
                if int.from_bytes(self.file.read(1), "big") == 0xd9:
                    break

        print("Wykryto dane binarne zdjęcia")

    ############################################################################################

    def skip_chunk(self):

        chunk_len = self.read_chunk_nl() -2
        test = self.file.read(chunk_len)

        print("Wykryto jakiś inny chunk o długości " + str(chunk_len))