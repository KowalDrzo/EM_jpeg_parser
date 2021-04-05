
class PictureInfo:


    ############################################################################################

    def __init__(self):
        pass

    def __del__(self):
        pass

    ############################################################################################

    def read_chunk_name(self, file) -> int:
        chunk_name = file.read(2)
        print(chunk_name)
        return int.from_bytes(chunk_name, "big")

    ############################################################################################

    def check_soi(self, file):

        int_byte = self.read_chunk_name()

        if int_byte != 0xffd8:
            
            print("Niepoprawny JPEG!")
            raise IOError

    ############################################################################################

    def read_adh(self, file):

        chunk_len = int.from_bytes(file.read(2), "big")
        file.read(chunk_len)

        print("Wykryto chunk ADH")

    ############################################################################################

    def read_qt(self, file):

        chunk_len = int.from_bytes(file.read(2), "big")
        file.read(chunk_len)

        print("Wykryto chunk QT")

    ############################################################################################

    def read_sof(self, file):

        chunk_len = int.from_bytes(file.read(2), "big")
        file.read(chunk_len)

        print("Wykryto chunk SOF")

    ############################################################################################

    def read_dht(self, file):

        chunk_len = int.from_bytes(file.read(2), "big")
        file.read(chunk_len)

        print("Wykryto chunk DHT")
    
    ############################################################################################

    def read_image(self, file):

        chunk_len = int.from_bytes(file.read(2), "big")
        file.read(chunk_len)

        print("Wykryto dane binarne zdjęcia")

    ############################################################################################

    def skipchunk(self, file):

        chunk_len = int.from_bytes(file.read(2), "big")
        file.read(chunk_len)

        print("Wykryto jakiś inny chunk o długości " + str(chunk_len))