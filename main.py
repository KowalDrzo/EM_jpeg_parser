#!/usr/bin/python3
import fft1
import show
import parser

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
file_name = show.check_file()

# Obsługa menu
while 1:

    print_menu()
    choice = input("Wybrano: ")


    if choice == "1":
        show.show_image(file_name)

    elif choice == "2":
        parser.parse_jpg(file_name)

    elif choice == "3":
        fft1.fourier(file_name)

    elif choice == "4":
        pass

    elif choice == "5":
        break
    else:
        print("Błędny wybór")