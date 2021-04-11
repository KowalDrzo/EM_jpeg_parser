import picture_info as pinf

"""
Funkcja parse_jpg służy do czytania kolejnych kodów nazw chunków i importowaniu metod parsujących te chunki.
"""

def parse_jpg(pic_inf):

    for i in range(2, len(pic_inf.binary_file) -1):
        if pic_inf.binary_file[i] == 0xff:

            next_byte = pic_inf.binary_file[i+1]
            if next_byte == 0x00: # Brak nowego chunka
                continue

            elif next_byte == 0xe0: # Chunk Application default header
                pic_inf.read_adh(i+2)

            elif next_byte == 0xdb: # Chunk z tabelą kwantyzacji
                pic_inf.read_qt(i+2)

            elif next_byte == 0xc0: # Chunk Start of frame
                pic_inf.read_sof(i+2)

            elif next_byte == 0xc2: # Chunk Start of frame 2
                pic_inf.read_sof2(i+2)

            elif next_byte == 0xc4: # Chunk z tabelą Huffmanna
                pic_inf.read_dht(i+2)

            elif next_byte == 0xe1: # Chunk Exif
                pic_inf.read_exif(i+2)

            elif next_byte == 0xe4: # Chunk APP4
                pic_inf.read_app4(i+2)

            elif next_byte == 0xdd: # Chunk resetu
                pic_inf.read_reset(i+2)

            elif next_byte == 0xfe: # Chunk z komentarzem
                pic_inf.read_comment(i+2)

            elif next_byte == 0xe2: # Chunk ICC
                pic_inf.read_icc(i+2)

            elif next_byte == 0xda: # Chunk Start of Scan i dane zdjęcia
                pic_inf.read_image(i+2)
            
            elif next_byte == 0xd9: # Koniec JPEGa
                break

            else:   # Pomijanie nieznanego chunka
                pic_inf.skip_chunk(pic_inf.binary_file[i+1], (i+2))
                

    print("Zakończono parsowanie pliku")

############################################################################################

def more_info_jpg(pic_inf):

    pass

############################################################################################

def save_jpg(pic_inf):

    name = input("Podaj nazwę nowego pliku: ")

    new_file = open(name, "wb")

    new_file.write(bytes(pic_inf.binary_file)) # Tymczasowo

    """
    new_file.write(0xffd8.to_bytes(2, "big"))

    for byte in pic_inf.binary_image:
        new_file.write(byte.to_bytes(1, "big"))

    new_file.write(0xffd9.to_bytes(2, "big"))
    """

    new_file.close()