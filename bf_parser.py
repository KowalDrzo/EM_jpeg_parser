import picture_info as pinf

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

############################################################################################

def more_info_jpg(pic_inf):

    pass

############################################################################################

def save_jpg(pic_inf, new_name):

    new_file = open(new_name, "wb")

    # Początek pliku:
    new_file.write(bytes([0xff, 0xd8]))

    if pic_inf.sof_chunk != None: # Dla plików JPEG ze zwykłym Start of Frame

        for qtable in pic_inf.quanti_tables: # Zapisywanie tabel kwantyzacji
            new_file.write(bytes([0xff, 0xdb]))
            new_file.write(bytes(pic_inf.binary_file[qtable.begin_ind:qtable.end_ind]))

        # Zapisywanie sof:
        new_file.write(bytes([0xff, 0xc0]))
        new_file.write(bytes(pic_inf.binary_file[pic_inf.sof_chunk.begin_ind:pic_inf.sof_chunk.end_ind]))

        # Zapisywanie sos:
        new_file.write(bytes([0xff, 0xda]))
        new_file.write(bytes(pic_inf.binary_file[pic_inf.binary_image_scan[0].begin_ind:pic_inf.binary_image_scan[0].end_ind]))

    elif pic_inf.sof2_chunk != None:

        for qtable in pic_inf.quanti_tables: # Zapisywanie tabel kwantyzacji
            new_file.write(bytes([0xff, 0xdb]))
            new_file.write(bytes(pic_inf.binary_file[qtable.begin_ind:qtable.end_ind]))

        # Zapisywanie sof:
        new_file.write(bytes([0xff, 0xc2]))
        new_file.write(bytes(pic_inf.binary_file[pic_inf.sof2_chunk.begin_ind:pic_inf.binary_image_scan[-1].end_ind]))


    # Koniec pliku:
    new_file.write(bytes([0xff, 0xd9]))

    new_file.close()