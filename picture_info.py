from chunks.jpeg_chunk import Chunk
import chunks.adh as adh
import chunks.sof as sof
import chunks.exif as exif
import chunks.sos as sos

"""
Klasa PictureInfo ...
"""

class PictureInfo:

    # Nazwa i zawartość pliku:
    file_name = ""
    binary_file = []

    # Obowiązkowe chunki:
    binary_image_scan = None
    quanti_tables = []
    sof_chunk = None

    # Dodatkowe chunki:
    adh_chunk = None
    exif_chunks = []
    huffmann_tables = []
    comments = []
    sof2_chunk = None
    app4 = None
    icc = None

    ############################################################################################

    def __init__(self, file_name):
        self.file_name = file_name
        file = open(file_name, "rb")
        self.binary_file = list(file.read())
        file.close()

    ############################################################################################

    def chunk_len(self, b_ind) -> int:
        return (self.binary_file[b_ind] << 8) | self.binary_file[b_ind +1]

    ############################################################################################

    def check_soi(self):

        start_not_detected = self.binary_file[0] != 0xff or self.binary_file[1] != 0xd8

        if start_not_detected:
            
            print("Niepoprawny JPEG!")
            raise IOError

    ############################################################################################
    ############################################################################################
    ############################################################################################
    
    def read_adh(self, b_ind):

        length = self.chunk_len(b_ind)
        self.adh_chunk = adh.ADH_chunk(b_ind, b_ind + length)

        print("Wykryto chunk Application default header długości " + str(length))

    ############################################################################################
    
    def read_qt(self, b_ind):

        length = self.chunk_len(b_ind)
        self.quanti_tables.append(Chunk(b_ind, b_ind + length))

        print("Wykryto chunk z tabelą kwantyzacji długości " + str(length))

    ############################################################################################
    
    def read_sof(self, b_ind):

        length = self.chunk_len(b_ind)
        self.sof_chunk = sof.SOF_chunk(b_ind, b_ind + length)

        print("Wykryto chunk Start of frame długości " + str(length))

    ############################################################################################

    def read_sof2(self, b_ind):

        length = self.chunk_len(b_ind)
        self.sof2_chunk = Chunk(b_ind, b_ind + length)

        print("Wykryto chunk Start of frame 2 długości " + str(length))

    ############################################################################################
    
    def read_dht(self, b_ind):

        length = self.chunk_len(b_ind)
        self.huffmann_tables.append(Chunk(b_ind, b_ind + length))

        print("Wykryto chunk z tabelą Huffmanna długości " + str(length))
    
    ############################################################################################
    
    def read_exif(self, b_ind):

        length = self.chunk_len(b_ind)
        self.exif_chunks.append(exif.EXIF_chunk(b_ind, b_ind + length))

        print("Wykryto chunk Exif długości " + str(length))

    ############################################################################################
    
    def read_app4(self, b_ind):

        length = self.chunk_len(b_ind)
        self.app4 = Chunk(b_ind, b_ind + length)

        print("Wykryto chunk APP4 długości " + str(length))
    
    ############################################################################################
    
    def read_reset(self, b_ind):

        length = self.chunk_len(b_ind)
        print("Wykryto chunk resetujący długości " + str(length))

    ############################################################################################
    
    def read_comment(self, b_ind):

        length = self.chunk_len(b_ind)
        
        comm = "".join([chr(c) for c in self.binary_file[b_ind:b_ind + length]])
        self.comments.append(comm)

        print("Wykryto chunk komentarza długości " + str(length))

    ############################################################################################

    def read_icc(self, b_ind):

        length = self.chunk_len(b_ind)
        self.icc = Chunk(b_ind, b_ind + length)

        print("Wykryto chunk ICC długości " + str(length))
    
    ############################################################################################
    ############################################################################################
    ############################################################################################

    def read_image(self, b_ind):

        e_ind = 0

        for j in range(b_ind ,len(self.binary_file) -1):
            
            if self.binary_file[j] == 0xff:
                if self.binary_file[j+1] != 0x00:
                    e_ind = j

        self.binary_image_scan = sos.SOS_chunk(b_ind, e_ind)

        print("Wykryto chunk Start skanu oraz skompresowane dane zdjęcia")
    
    ############################################################################################

    def skip_chunk(self, number, b_ind):

        length = self.chunk_len(b_ind)
        print(str(number) + ": Wykryto jakiś inny chunk o długości " + str(length))