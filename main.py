import fft1

"""
Funkcja print_menu do wyświetlania menu głównego programu.
"""
def print_menu():

    print("""
    1. Wyświetl obraz
    2. Wypisz informacje o obrazie
    3. Wyświetl transformatę obrazu
    4. Zapisz obraz usuwając metadane
    5. Wyjdź

    Wybrano:""")

############################################################################################

"""
Główny kod programu - obsługa menu.
"""

print("\nProgram do parsowania plików JPEG. Podaj nazwę pliku do wczytania:")
file_name = input()

while 1:

    print_menu()
    choice = input()


    if choice == "1":
        pass

    elif choice == "2":
        pass

    elif choice == "3":
        fft1.fourier(file_name)

    elif choice == "4":
        pass

    elif choice == "5":
        break
    else:
        print("Błędny wybór")