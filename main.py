#!/usr/bin/python3
from gui import *


"""
Główny kod programu.
"""

# Sprawdzanie poprawności otworzenia pliku - także tego, czy pierwsze 2 bajty są 0xFFD8
file_name = show.check_file(sys.argv)

pic_inf = pinf.PictureInfo(file_name)
pic_inf.check_soi()

# Przeparsowanie pliku:
#bf_parser.parse_jpg(pic_inf)

# Wyświetlenie menu:
menu = GuiMenu(pic_inf)
menu.display_menu()