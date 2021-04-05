import picture_info as pinf

"""
Funkcja parse_jpg służy do parsowania pliku jpg celem wyciągnięcia informacji o obrazie
"""

def parse_jpg(file_name):

    pic_inf = pinf.PictureInfo(file_name)
    pic_inf.check_soi()

    while True:

        chunk = pic_inf.read_chunk_nl()

        if chunk == 0xffe0:
            pic_inf.read_adh()

        elif chunk == 0xffdb:
            pic_inf.read_qt()

        elif chunk == 0xffc0:
            pic_inf.read_sof()

        elif chunk == 0xffc4:
            pic_inf.read_dht()

        elif chunk == 0xffda:
            pic_inf.read_image()
            break
        
        #elif chunk == 0xffd9:
         #   break

        else:
            pic_inf.skip_chunk()

    print("Koniec pliku")