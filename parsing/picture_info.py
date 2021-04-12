from chunks.jpeg_chunk import Chunk
import chunks.adh as adh
import chunks.app4 as app4
import chunks.exif as exif
import chunks.icc as icc
import chunks.sof as sof
import chunks.sos as sos


"""
Klasa PictureInfo OPIS TODO!!!
"""

class PictureInfo:

    # Nazwa i zawartość pliku:
    file_name = ""
    binary_file = []

    # Obowiązkowe chunki:
    binary_image_scan = []
    quanti_tables = []
    sof_chunk = None

    # Dodatkowe chunki:
    adh_chunk = None
    exif_chunks = []
    huffmann_tables = []
    comments = []
    app4_chunk = None
    icc_chunk = None

    ############################################################################################

    """
    OPIS TODO!!!
    """

    def __init__(self, file_name):
        self.file_name = file_name
        file = open(file_name, "rb")
        self.binary_file = list(file.read())
        file.close()

    ############################################################################################

    """
    OPIS TODO!!!
    """

    def chunk_len(self, b_ind) -> int:
        return (self.binary_file[b_ind] << 8) | self.binary_file[b_ind +1]

    ############################################################################################

    """
    OPIS TODO!!!
    """

    def check_soi(self):

        start_not_detected = self.binary_file[0] != 0xff or self.binary_file[1] != 0xd8

        if start_not_detected:
            
            print("Niepoprawny JPEG!")
            raise IOError

    ############################################################################################
    ############################################################################################
    ############################################################################################
    
    def read_adh(self, b_ind) -> int:

        length = self.chunk_len(b_ind)
        self.adh_chunk = adh.ADH_chunk(b_ind, b_ind + length)
        self.adh_chunk.get_info(self.binary_file[b_ind:b_ind + length])

        print("Wykryto chunk Application default header długości " + str(length))
        return b_ind + length

    ############################################################################################
    
    def read_qt(self, b_ind) -> int:

        length = self.chunk_len(b_ind)
        self.quanti_tables.append(Chunk(b_ind, b_ind + length))

        print("Wykryto chunk z tabelą kwantyzacji długości " + str(length))
        return b_ind + length

    ############################################################################################
    
    def read_sof(self, b_ind, number) -> int:

        length = self.chunk_len(b_ind)
        self.sof_chunk = sof.SOF_chunk(b_ind, b_ind + length)
        self.sof_chunk.get_info(self.binary_file[b_ind:b_ind + length], number)

        print("Wykryto chunk Start of frame (typ " + str(self.sof_chunk.sof_nb) + ") długości " + str(length))
        return b_ind + length

    ############################################################################################
    
    def read_dht(self, b_ind) -> int:

        length = self.chunk_len(b_ind)
        self.huffmann_tables.append(Chunk(b_ind, b_ind + length))

        print("Wykryto chunk z tabelą Huffmanna długości " + str(length))
        return b_ind + length
    
    ############################################################################################
    
    def read_exif(self, b_ind) -> int:

        length = self.chunk_len(b_ind)
        self.exif_chunks.append(exif.EXIF_chunk(b_ind, b_ind + length))
        
        for exif_ch in self.exif_chunks:
            exif_ch.get_info(self.binary_file[b_ind:b_ind + length])

        print("Wykryto chunk Exif długości " + str(length))
        return b_ind + length

    ############################################################################################
    
    def read_app4(self, b_ind) -> int:

        length = self.chunk_len(b_ind)
        self.app4_chunk = app4.APP4_chunk(b_ind, b_ind + length)
        self.app4_chunk.get_info(self.binary_file[b_ind:b_ind + length])

        print("Wykryto chunk APP4 długości " + str(length))
        return b_ind + length
    
    ############################################################################################
    
    def read_reset(self, b_ind) -> int:

        length = self.chunk_len(b_ind)
        print("Wykryto chunk resetujący długości " + str(length))
        return b_ind + length

    ############################################################################################
    
    def read_comment(self, b_ind) -> int:

        length = self.chunk_len(b_ind)
        
        comm = "".join([chr(c) for c in self.binary_file[b_ind:b_ind + length]])
        self.comments.append(comm)

        print("Wykryto chunk komentarza długości " + str(length))
        return b_ind + length

    ############################################################################################

    def read_icc(self, b_ind) -> int:

        length = self.chunk_len(b_ind)
        self.icc = icc.ICC_chunk(b_ind, b_ind + length)
        self.icc.get_info(self.binary_file[b_ind:b_ind + length])

        print("Wykryto chunk ICC długości " + str(length))
        return b_ind + length
    
    ############################################################################################
    ############################################################################################
    ############################################################################################
    
    """
    OPIS TODO!!!
    """

    def read_image(self, b_ind) -> int:

        e_ind = 0
        res_counter = 0
        header_length = self.chunk_len(b_ind)

        for j in range(b_ind+1 ,len(self.binary_file) -1):  
            if self.binary_file[j] == 0xff:
                if self.binary_file[j+1] != 0x00:
                    
                    if self.binary_file[j+1] >= 0xd0 and self.binary_file[j+1] <= 0xd7:
                        res_counter += 1
                    else:
                        e_ind = j
                        break

        self.binary_image_scan.append(sos.SOS_chunk(b_ind, e_ind))
        self.binary_image_scan[-1].get_info(self.binary_file[b_ind:b_ind + header_length])

        print("Wykryto chunk Start skanu oraz skompresowane dane zdjęcia")
        return e_ind
    
    ############################################################################################

    """
    OPIS TODO!!!
    """

    def skip_chunk(self, number, b_ind) -> int:

        length = self.chunk_len(b_ind)

        print(str(number) + ": Wykryto jakiś inny chunk o długości " + str(length) + " Początek: " + str(b_ind))
        return b_ind + length