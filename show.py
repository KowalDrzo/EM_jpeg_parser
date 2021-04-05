import cv2

"""
Funkcja show_image służy do wyświetlenia obrazu.
"""

def show_image(file_name):

    img = cv2.imread(file_name)
    cv2.imshow("Obraz", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

############################################################################################

"""
Funkcja check_file, sprawdza czy plik o podanej nazwie jest dostępny, jeśli nie, to prosi o nową nazwę. Na koniec zwraca prawidłową nazwę.
"""

def check_file(args: list) -> str:

    if len(args) > 1:
        print("Plik czytany z argumentu: " + args[1] + "\n\n")
        try:
            file = open(args[1], "rb")
        except IOError:
            print("Błędna nazwa pliku w argumencie!\n\n")
        else:
            return args[1]

    while 1:

        file_name = input("Podaj nazwę pliku do wczytania: ")

        try:
            file = open(file_name, "rb")
        except IOError:
            print("Błędna nazwa pliku")
            continue

        file.close()
        break
    return file_name