import picture_info as pinf

"""
Funkcja parse_jpg służy do parsowania pliku jpg celem wyciągnięcia informacji o obrazie
"""

def parse_jpg(file_name):
    
    pic_inf = pinf.PictureInfo(file_name)

    pic_inf.check_soi()
