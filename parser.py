
"""
Funkcja parse_jpg służy do parsowania pliku jpg celem wyciągnięcia informacji o obrazie
"""

def parse_jpg(file_name):

    file = open(file_name, "rb")
    content = file.read()
    file.close()

    print (content)