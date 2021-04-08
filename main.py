#!/usr/bin/python3
from gui import *


"""
Główny kod programu.
"""
print("\nProgram do parsowania plików JPEG")

# Sprawdzanie poprawności otworzenia pliku
file_name = show.check_file(sys.argv)

pic_inf = pinf.PictureInfo(file_name)
pic_inf.check_soi()
parser.parse_jpg(pic_inf)

menu = GuiMenu(pic_inf)

menu.display_menu()