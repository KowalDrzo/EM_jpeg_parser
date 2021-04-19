"""
OPIS TODO!!!
"""

def save_jpg(pic_inf, new_name):

    new_file = open(new_name, "wb")

    # Początek pliku:
    new_file.write(bytes([0xff, 0xd8]))

    for qtable in pic_inf.quanti_tables: # Zapisywanie tabel kwantyzacji
        new_file.write(bytes([0xff, 0xdb]))
        new_file.write(bytes(pic_inf.binary_file[qtable.begin_ind:qtable.end_ind]))

    # Zapisywanie sof:
    new_file.write(bytes([0xff, 0xc0]))
    new_file.write(bytes(pic_inf.binary_file[pic_inf.sof_chunk.begin_ind:pic_inf.sof_chunk.end_ind]))

    # Zapisywanie sos:
    if pic_inf.sof_chunk.sof_nb == 0:
        for sos in pic_inf.binary_image_scan:
            new_file.write(bytes([0xff, 0xda]))
            new_file.write(bytes(pic_inf.binary_file[sos.begin_ind:sos.end_ind]))

    elif pic_inf.sof_chunk.sof_nb == 2:

        new_file.write(bytes([0xff, 0xc4]))
        new_file.write(bytes(pic_inf.binary_file[pic_inf.huffmann_tables[0].begin_ind:pic_inf.huffmann_tables[0].end_ind]))

        for i in range(0, len(pic_inf.binary_image_scan)):
            new_file.write(bytes([0xff, 0xc4]))
            new_file.write(bytes(pic_inf.binary_file[pic_inf.huffmann_tables[i+1].begin_ind:pic_inf.huffmann_tables[i+1].end_ind]))
            
            new_file.write(bytes([0xff, 0xda]))
            new_file.write(bytes(pic_inf.binary_file[pic_inf.binary_image_scan[i].begin_ind:pic_inf.binary_image_scan[i].end_ind]))


    # Koniec pliku:
    new_file.write(bytes([0xff, 0xd9]))

    new_file.close()