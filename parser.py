import picture_info as pinf

"""
Funkcja parse_jpg służy do parsowania pliku jpg celem wyciągnięcia informacji o obrazie
"""

def parse_jpg(file_name):
    
    file = open(file_name, "rb")

    pic_inf = pinf.PictureInfo()
    pic_inf.check_soi(file)

    while True:

        chunk = pic_inf.read_chunk_name(file)

        if chunk == 0xffe0:
            pic_inf.read_adh(file)

        elif chunk == 0xffdb:
            pic_inf.read_qt(file)

        elif chunk == 0xffc0:
            pic_inf.read_sof(file)

        elif chunk == 0xffc4:
            pic_inf.read_dht(file)

        elif chunk == 0xffda:
            pic_inf.read_image(file)
        
        elif chunk == 0xffd9:
            break

        else:
            pic_inf.skipchunk(file)

    print("Koniec pliku")
    file.close()