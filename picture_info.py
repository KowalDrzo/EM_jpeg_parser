from chunks.chunk import Chunk
import chunks.adh as adh


class PictureInfo:

    file_name = ""
    binary_file = []

    binary_image_scan = None
    quanti_tables = []
    sof = None

    adh_chunk = None
    
    comments = []

    ############################################################################################

    def __init__(self, file_name):
        self.file_name = file_name
        file = open(file_name, "rb")
        self.binary_file = list(file.read())
        file.close()

    ############################################################################################

    #def read_chunk_nl(self) -> int:
     #   return int.from_bytes(self.file.read(2), "big")

    ############################################################################################

    def check_soi(self):

        if self.binary_file[0] != 0xff or self.binary_file[1] != 0xd8:
            
            print("Niepoprawny JPEG!")
            raise IOError

    ############################################################################################
    ############################################################################################
    ############################################################################################
    """
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

    """
        