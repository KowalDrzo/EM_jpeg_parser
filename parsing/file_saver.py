"""
OPIS TODO!!!
"""

def save_jpg(pic_inf, new_name):

    new_file = open(new_name, "wb")

    # Początek pliku:
    new_file.write(bytes([0xff, 0xd8]))

    for nec_chunk in pic_inf.necessary_chunks:
        new_file.write(bytes([0xff, nec_chunk.marker]))
        new_file.write(bytes(pic_inf.binary_file[nec_chunk.begin_ind:nec_chunk.end_ind]))

    # Koniec pliku:
    new_file.write(bytes([0xff, 0xd9]))

    new_file.close()