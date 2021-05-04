from chunks.jpeg_chunk import Chunk
import chunks.adh as adh
import chunks.exif as exif
import chunks.sof as sof
import chunks.sos as sos

is_huffmann_necessary = True

"""
Klasa PictureInfo OPIS TODO!!!
"""

class PictureInfo:

    # Nazwa i zawartość pliku:
    file_name = ""
    binary_file = []

    # Obowiązkowe chunki:
    necessary_chunks = []

    # Dodatkowe chunki:
    metadata_chunks = []
    comments    = []

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
    
    # Chunk opcjonalny:
    def read_adh(self, b_ind) -> int:

        length = self.chunk_len(b_ind)
        self.metadata_chunks.append(adh.ADH_chunk(b_ind, b_ind + length))
        self.metadata_chunks[-1].get_info(self.binary_file[b_ind:b_ind + length])

        print("Wykryto chunk Application default header długości " + str(length))
        return b_ind + length

    ############################################################################################
    
    # Chunk obowiązkowy:
    def read_qt(self, b_ind) -> int:

        length = self.chunk_len(b_ind)
        self.necessary_chunks.append(Chunk(b_ind, b_ind + length, 0xdb))

        print("Wykryto chunk z tabelą kwantyzacji długości " + str(length))
        return b_ind + length

    ############################################################################################
    
    # Chunk obowiązkowy:
    def read_sof(self, b_ind, marker) -> int:

        length = self.chunk_len(b_ind)

        self.necessary_chunks.append(sof.SOF_chunk(b_ind, b_ind + length, marker))
        self.necessary_chunks[-1].get_info(self.binary_file[b_ind:b_ind + length], marker & 0x0f)

        print("Wykryto chunk Start of frame (typ " + str(marker & 0x0f) + ") długości " + str(length))
        return b_ind + length

    ############################################################################################
    
    # Chunk zwykle obowiązkowy (choć bywają wyjątki):
    def read_dht(self, b_ind) -> int:

        length = self.chunk_len(b_ind)
        
        if is_huffmann_necessary:
            self.necessary_chunks.append(Chunk(b_ind, b_ind + length, 0xc4))
        else:
            self.metadata_chunks.append(Chunk(b_ind, b_ind + length, 0xc4))

        print("Wykryto chunk z tabelą Huffmanna długości " + str(length))
        return b_ind + length
    
    ############################################################################################
    
    # Chunk opcjonalny:
    def read_exif(self, b_ind) -> int:

        length = self.chunk_len(b_ind)

        self.metadata_chunks.append(exif.EXIF_chunk(b_ind, b_ind + length))
        self.metadata_chunks[-1].parse_exif(self.binary_file[b_ind:b_ind + length])

        print("Wykryto chunk Exif długości " + str(length))
        return b_ind + length

    ############################################################################################
    
    # Chunk opcjonalny - stosunkowo rzadki i specjalistyczny. Ten program nie zagłębia się w jego parsowanie:
    def read_app4(self, b_ind) -> int:

        length = self.chunk_len(b_ind)

        self.metadata_chunks.append(Chunk(b_ind, b_ind + length))

        print("Wykryto chunk APP4 długości " + str(length))
        return b_ind + length
    
    ############################################################################################
    
    # Chunk obowiązkowy:
    def read_reset(self, b_ind) -> int:

        length = self.chunk_len(b_ind)

        self.necessary_chunks.append(Chunk(b_ind, b_ind + length, 0xdd))

        print("Wykryto chunk interwału resetów długości " + str(length))
        return b_ind + length

    ############################################################################################
    
    # Chunk opcjonalny:
    def read_comment(self, b_ind) -> int:

        length = self.chunk_len(b_ind)
        
        comm = "".join([chr(c) for c in self.binary_file[b_ind:b_ind + length]])
        self.comments.append(comm)

        print("Wykryto chunk komentarza długości " + str(length))
        return b_ind + length

    ############################################################################################

    # Chunk opcjonalny - stosunkowo rzadki i specjalistyczny. Ten program nie zagłębia się w jego parsowanie:
    def read_icc(self, b_ind) -> int:

        length = self.chunk_len(b_ind)
        
        self.metadata_chunks.append(Chunk(b_ind, b_ind + length))

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

        self.necessary_chunks.append(sos.SOS_chunk(b_ind, e_ind, 0xda))
        self.necessary_chunks[-1].get_info(self.binary_file[b_ind:b_ind + header_length])

        print("Wykryto chunk Start skanu oraz skompresowane dane zdjęcia")
        return e_ind
    
    ############################################################################################

    """
    Funkcja pomijająca nieznany chunk i wypisująca jego rozmiar.

    Param:
    number - numer definiujący typ nieznanego chunka,
    b_ind - indeks początku chunka (pierwszy indeks rozmiaru).

    Returns:
    int - indeks pierwszego elementu za tym chunkiem.
    """

    def skip_chunk(self, number, b_ind) -> int:

        length = self.chunk_len(b_ind)

        print(str(number) + ": Wykryto jakiś inny chunk o długości " + str(length) + " Początek: " + str(b_ind))
        return b_ind + length