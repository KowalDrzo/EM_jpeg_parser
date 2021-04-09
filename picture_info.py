import chunks.adh as adh

class PictureInfo:

    file_name = ""
    file = None
    binary_image = []
    adh_chunk = adh.ADH_chunk()
    comment_chunk = []

    ############################################################################################

    def __init__(self, file_name):
        self.file_name = file_name
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
    ############################################################################################
    ############################################################################################

    def read_adh(self):

        chunk_len = self.read_chunk_nl()
        test = self.file.read(chunk_len - 2)

        print("Wykryto chunk Application default header długości " + str(chunk_len))

    ############################################################################################

    def read_qt(self):

        chunk_len = self.read_chunk_nl()
        test = self.file.read(chunk_len - 2)

        print("Wykryto chunk z tabelą kwantyzacji długości " + str(chunk_len))

    ############################################################################################

    def read_sof(self):

        chunk_len = self.read_chunk_nl()
        test = self.file.read(chunk_len - 2)

        print("Wykryto chunk Start of frame długości " + str(chunk_len))

    ############################################################################################

    def read_dht(self):

        chunk_len = self.read_chunk_nl()
        test = self.file.read(chunk_len - 2)

        print("Wykryto chunk z tabelą Huffmann długości " + str(chunk_len))
    
    ############################################################################################

    def read_exif(self):

        chunk_len = self.read_chunk_nl()
        test = self.file.read(chunk_len - 2)

        print("Wykryto chunk Exif długości " + str(chunk_len))

    ############################################################################################

    def read_app4(self):

        chunk_len = self.read_chunk_nl()
        test = self.file.read(chunk_len - 2)

        print("Wykryto chunk APP4 długości " + str(chunk_len))

    ############################################################################################

    def read_reset(self):

        chunk_len = self.read_chunk_nl()
        test = self.file.read(chunk_len - 2)

        print("Wykryto chunk resetujący długości " + str(chunk_len))

    ############################################################################################

    def read_comment(self):

        chunk_len = self.read_chunk_nl()
        comm = self.file.read(chunk_len - 2)
        self.comment_chunk.append(comm.decode("ascii"))

        print(self.comment_chunk)

        print("Wykryto chunk komentarza długości " + str(chunk_len))

    ############################################################################################

    def read_icc(self):

        chunk_len = self.read_chunk_nl()
        test = self.file.read(chunk_len - 2)

        print("Wykryto chunk ICC długości " + str(chunk_len))

    ############################################################################################

    def read_sof2(self):

        chunk_len = self.read_chunk_nl()
        test = self.file.read(chunk_len - 2)

        print("Wykryto chunk Start of frame 2 długości " + str(chunk_len))

    ############################################################################################
    ############################################################################################
    ############################################################################################

    def read_image(self):

        chunk_len = self.read_chunk_nl()
        test = self.file.read(chunk_len - 2)

        print("Wykryto chunk Start skanu oraz skompresowane dane zdjęcia")

        data_bit = 1
        while True:

            data_bit = int.from_bytes(self.file.read(1), "big")

            if data_bit == 0xff:
                data_bit = int.from_bytes(self.file.read(1), "big")
                if data_bit == 0x00:
                    self.binary_image.append(0xff)
                else:
                    break
            
            self.binary_image.append(data_bit)

    ############################################################################################

    def skip_chunk(self, name):

        chunk_len = self.read_chunk_nl()
        test = self.file.read(chunk_len - 2)

        print(str(name) + ": Wykryto jakiś inny chunk o długości " + str(chunk_len))