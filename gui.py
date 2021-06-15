from numpy.core.arrayprint import set_string_function
import fft1
import show
import parsing.picture_info as pinf

from parsing.bf_parser  import parse_jpg
from parsing.file_saver import save_jpg
from parsing.more_info  import more_info_jpg
from encrypting.szyfrowanie_RSA import Encryptor
import encrypting.not_compressed_enc as nc_enc

from tkinter import *
import tkinter.filedialog as fd

############################################################################################

"""
OPIS TODO!!!
"""

class GuiMenu:

    pic_inf = None
    encryptor_rsa = None

    main_window = Tk()
    key_entry = Entry(main_window)
    N_entry = Entry(main_window)
    check_tabs = BooleanVar()

    def __init__(self, pic_inf, encryptor):
        self.pic_inf = pic_inf
        self.encryptor_rsa = encryptor

    """
    OPIS TODO!!!
    """

    def display_menu(self):
        
        self.main_window.geometry("640x480")
        self.main_window.title("JPEG Parser")
        
        b_width = 32
        option1 = Button(self.main_window, width = b_width, text ="Wyświetl obraz",                          command = self.option1_callback)
        option2 = Button(self.main_window, width = b_width, text ="Wypisz informacje o obrazie",             command = self.option2_callback)
        option3 = Button(self.main_window, width = b_width, text ="Wyświetl transformatę obrazu",            command = self.option3_callback)
        option4 = Button(self.main_window, width = b_width, text ="Zapisz obraz usuwając zbędne metadane",   command = self.option4_callback)
        option5 = Button(self.main_window, width = b_width, text ="Wygeneruj klucze RSA",                    command = self.option5_callback)
        option6 = Button(self.main_window, width = b_width, text ="Zaszyfruj obraz",                         command = self.option6_callback)
        option7 = Button(self.main_window, width = b_width, text ="Odszyfruj obraz",                         command = self.option7_callback)
        option8 = Button(self.main_window, width = b_width, text ="Szyfrowanie nieskompresowanego...",       command = self.option8_callback)
        option_exit = Button(self.main_window, width = b_width, text ="Wyjdź",                               command = self.option_exit_callback)
        
        tabs_box = Checkbutton(self.main_window,  text="Szyfrowanie także tabel kwantyzacji i huffmanna",     variable = self.check_tabs)
        key_text = Label(self.main_window, text="Klucz:")
        N_text = Label(self.main_window, text="N:")

        option1.pack()
        option2.pack()
        option3.pack()
        option4.pack()
        option5.pack()
        option6.pack()
        option7.pack()
        option8.pack()

        tabs_box.pack()
        key_text.pack()
        self.key_entry.pack()
        N_text.pack()
        self.N_entry.pack()
        option_exit.pack()

        self.main_window.mainloop()

    ############################################################################################

    def option1_callback(self):
        show.show_image(self.pic_inf.file_name)

    def option2_callback(self):
        more_info_jpg(self.pic_inf)

    def option3_callback(self):
        fft1.fourier(self.pic_inf.file_name)

    def option4_callback(self):
        new_name = fd.asksaveasfilename()
        save_jpg(self.pic_inf, new_name)

    def option5_callback(self):
        N_entry_texts = self.encryptor_rsa.showGeneratedKeys()
        
        self.N_entry.delete(0, END)
        self.N_entry.insert(0, N_entry_texts[0])
        
        self.key_entry.delete(0, END)
        self.key_entry.insert(0, N_entry_texts[1])

    def option6_callback(self):
        new_name = fd.asksaveasfilename()
        self.encryptor_rsa.save_encrypted(self.pic_inf, new_name, int(self.key_entry.get()), int(self.N_entry.get()), False, self.check_tabs.get())

    def option7_callback(self):
        new_name = fd.asksaveasfilename()
        self.encryptor_rsa.save_encrypted(self.pic_inf, new_name, int(self.key_entry.get()), int(self.N_entry.get()), True, self.check_tabs.get())

    def option8_callback(self):
        nc_enc.encrypt_not_compressed("Obraz/led1.jpg", "Obraz/testowy4.jpg", int(self.key_entry.get()), int(self.N_entry.get()))

    def option_exit_callback(self):
        exit()