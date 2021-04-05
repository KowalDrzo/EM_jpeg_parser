import chunks.adh as adh

class PictureInfo:

    file = None
    binary_image = []
    adh_chunk = adh.ADH_chunk()

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

        chunk_len = self.read_chunk_nl()
        test = self.file.read(chunk_len - 2)

        print("Wykryto chunk ADH długości " + str(chunk_len))

    ############################################################################################

    def read_qt(self):

        chunk_len = self.read_chunk_nl()
        test = self.file.read(chunk_len - 2)

        print("Wykryto chunk QT długości " + str(chunk_len))

    ############################################################################################

    def read_sof(self):

        chunk_len = self.read_chunk_nl()
        test = self.file.read(chunk_len - 2)

        print("Wykryto chunk SOF długości " + str(chunk_len))

    ############################################################################################

    def read_dht(self):

        chunk_len = self.read_chunk_nl()
        test = self.file.read(chunk_len - 2)

        print("Wykryto chunk DHT długości " + str(chunk_len))
    
    ############################################################################################

    def read_image(self):

        chunk_len = self.read_chunk_nl()
        test = self.file.read(chunk_len - 2)

        print("Wykryto dane binarne zdjęcia")

        data_bit = 1
        while True:

            data_bit = int.from_bytes(self.file.read(1), "big")

            if data_bit == 0xff:
                data_bit = int.from_bytes(self.file.read(1), "big")
                if data_bit == 0xd9:
                    break
                else:
                    self.binary_image.append(0xff)
            
            self.binary_image.append(data_bit)

        print("Wykryto koniec pliku")

    ############################################################################################

    def skip_chunk(self):

        chunk_len = self.read_chunk_nl()
        test = self.file.read(chunk_len - 2)

        print("Wykryto jakiś inny chunk o długości " + str(chunk_len))