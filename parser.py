import picture_info as pinf

"""
Funkcja parse_jpg służy do parsowania pliku jpg celem wyciągnięcia informacji o obrazie
"""

def parse_jpg(pic_inf):

    while True:

        chunk = pic_inf.read_chunk_nl()

        if chunk == 0xffe0:
            pic_inf.read_adh()

        elif chunk == 0xffdb:
            pic_inf.read_qt()

        elif chunk == 0xffc0:
            pic_inf.read_sof()

        elif chunk == 0xffc2:
            pic_inf.read_sof2()

        elif chunk == 0xffc4:
            pic_inf.read_dht()
        
        elif chunk == 0xffe1:
            pic_inf.read_exif()
        
        elif chunk == 0xffe4:
            pic_inf.read_app4()

        elif chunk == 0xffdd:
            pic_inf.read_reset()

        elif chunk == 0xfffe:
            pic_inf.read_comment()
        
        elif chunk == 0xffe2:
            pic_inf.read_icc()

        elif chunk == 0xffda:
            pic_inf.read_image()
            break

        else:
            pic_inf.skip_chunk(chunk)

    print("Zakończono parsowanie pliku")

############################################################################################

def more_info_jpg(pic_inf):

    pass

############################################################################################

def save_jpg(pic_inf):

    name = input("Podaj nazwę nowego pliku: ")

    new_file = open(name, "wb")

    new_file.write(0xffd8.to_bytes(2, "big"))

    new_file.write(0xffd9.to_bytes(2, "big"))

    new_file.close()