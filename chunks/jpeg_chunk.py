"""
Klasa Chunk zarządzająca umiejscowieniem danego chunka w pliku.
Chunk należy od begin_ind włącznie do end_ind wyłącznie.
"""

class Chunk:

    begin_ind = 0   # Indeks pierwszego bajtu chunku zaraz po jego nazwie (pierwszy bit rozmiaru chunku),
    end_ind = 0     # Indeks będący już poza chunkiem (tak aby range(begin_ind, end_ind) nie wzięło go pod uwagę),
    marker = 0      # Marker zaczynający chunk (opcjonalne).

    def __init__(self, b = -1, e = -1, mark = -1):
        self.begin_ind = b
        self.end_ind = e
        self.marker = mark