
class PictureInfo:

    SOI = False



"""
Funkcja parse_jpg służy do parsowania pliku jpg celem wyciągnięcia informacji o obrazie
"""

def parse_jpg(file_name):

    file = open(file_name, "rb")
    
    pic_inf = PictureInfo()

    chunk_name = file.read(2)
    int_byte = int.from_bytes(chunk_name, "big")

    if int_byte == 0xffd8:
        print("To jest JPG")
    else:
        print("To NIE jest JPG")

    file.close()