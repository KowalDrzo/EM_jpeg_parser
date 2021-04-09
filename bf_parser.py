import picture_info as pinf

"""
Funkcja parse_jpg służy do czytania kolejnych kodów nazw chunków i importowaniu metod parsujących te chunki.
"""

def parse_jpg(pic_inf):

    chunk = 1
    while True:

        chunk = pic_inf.read_chunk_nl()

        if chunk == 0xffe0: # Chunk Application default header
            pic_inf.read_adh()

        elif chunk == 0xffdb: # Chunk z tabelą kwantyzacji
            pic_inf.read_qt()

        elif chunk == 0xffc0: # Chunk Start of frame
            pic_inf.read_sof()

        elif chunk == 0xffc2: # Chunk Start of frame 2
            pic_inf.read_sof2()

        elif chunk == 0xffc4: # Chunk z tabelą Huffmanna
            pic_inf.read_dht()
        
        elif chunk == 0xffe1: # Chunk Exif
            pic_inf.read_exif()
        
        elif chunk == 0xffe4:
            pic_inf.read_app4() # Chunk APP4

        elif chunk == 0xffdd: # Chunk resetu
            pic_inf.read_reset()

        elif chunk == 0xfffe: # Chunk z komentarzem
            pic_inf.read_comment()
        
        elif chunk == 0xffe2: # Chunk ICC
            pic_inf.read_icc()

        elif chunk == 0xffda: # Chunk Start of Scan i dane zdjęcia
            pic_inf.read_image()

        elif chunk == 0xffd9 or chunk == 0: # Koniec pliku - marker końca lub fizyczny koniec pliku (w przypadku braku markera)
            break

        else:
            pic_inf.skip_chunk(chunk)

    print("Zakończono parsowanie pliku")

############################################################################################

def more_info_jpg(pic_inf):

    print(pic_inf.binary_image)
    pass

############################################################################################

def save_jpg(pic_inf):

    name = input("Podaj nazwę nowego pliku: ")

    new_file = open(name, "wb")

    new_file.write(0xffd8.to_bytes(2, "big"))

    for byte in pic_inf.binary_image:
        new_file.write(byte.to_bytes(1, "big"))

    new_file.write(0xffd9.to_bytes(2, "big"))

    new_file.close()