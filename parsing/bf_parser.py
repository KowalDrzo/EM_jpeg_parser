import parsing.picture_info as pinf

"""
Funkcja parse_jpg służy do czytania kolejnych kodów nazw chunków i importowaniu metod parsujących te chunki.
"""

def parse_jpg(pic_inf):

    i = 2

    while i < len(pic_inf.binary_file) -1:
        if pic_inf.binary_file[i] == 0xff:

            next_byte = pic_inf.binary_file[i+1]
            if next_byte == 0x00 or (next_byte >= 0xd0 and next_byte <= 0xd7): # Brak nowego chunka lub reset
                i += 2

            elif next_byte == 0xe0: # Chunk Application default header
                i = pic_inf.read_adh(i+2)

            elif next_byte == 0xdb: # Chunk z tabelą kwantyzacji
                i = pic_inf.read_qt(i+2)

            elif next_byte == 0xc0: # Chunk Start of frame
                i = pic_inf.read_sof(i+2)

            elif next_byte == 0xc2: # Chunk Start of frame 2
                i = pic_inf.read_sof2(i+2)

            elif next_byte == 0xc4: # Chunk z tabelą Huffmanna
                i = pic_inf.read_dht(i+2)

            elif next_byte == 0xe1: # Chunk Exif
                i = pic_inf.read_exif(i+2)

            elif next_byte == 0xe4: # Chunk APP4
                i = pic_inf.read_app4(i+2)

            elif next_byte == 0xdd: # Chunk resetu
                i = pic_inf.read_reset(i+2)

            elif next_byte == 0xfe: # Chunk z komentarzem
                i = pic_inf.read_comment(i+2)

            elif next_byte == 0xe2: # Chunk ICC
                i = pic_inf.read_icc(i+2)

            elif next_byte == 0xda: # Chunk Start of Scan i dane zdjęcia
                i = pic_inf.read_image(i+2)
            
            elif next_byte == 0xd9: # Koniec JPEGa
                break

            else:   # Pomijanie nieznanego chunka
                i = pic_inf.skip_chunk(pic_inf.binary_file[i+1], (i+2))
                

    print("Zakończono parsowanie pliku")