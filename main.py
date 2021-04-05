#!/usr/bin/python3
import fft1
import show
import parser
import sys
import picture_info as pinf

"""
Funkcja print_menu do wyświetlania menu głównego programu.
"""
def print_menu():

    print("""
    1. Wyświetl obraz
    2. Wypisz informacje o obrazie
    3. Wyświetl transformatę obrazu
    4. Zapisz obraz usuwając zbędne metadane
    5. Wyjdź
    """)

############################################################################################

"""
Główny kod programu - obsługa menu.
"""

print("\nProgram do parsowania plików JPEG")

# Sprawdzanie poprawności otworzenia pliku
file_name = show.check_file(sys.argv)

pic_inf = pinf.PictureInfo(file_name)
pic_inf.check_soi()
parser.parse_jpg(pic_inf)

# Obsługa menu
while 1:

    print_menu()
    choice = input("Wybrano: ")


    if choice == "1":
        show.show_image(file_name)

    elif choice == "2":
        parser.more_info_jpg(pic_inf)

    elif choice == "3":
        fft1.fourier(file_name)

    elif choice == "4":
        parser.save_jpg(pic_inf)

    elif choice == "5":
        break
    else:
        print("Błędny wybór")