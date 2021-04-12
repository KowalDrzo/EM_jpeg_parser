
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