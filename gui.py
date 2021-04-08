import fft1
import show
import parser
import sys
import picture_info as pinf
from tkinter import *

class GuiMenu:

    pic_inf = None

    def __init__(self, pic_inf):
        self.pic_inf = pic_inf

    def display_menu(self):
        
        main_window = Tk()
        main_window.geometry("640x480")
        main_window.title("JPEG Parser")
        
        b_width = 32
        option1 = Button(main_window, width = b_width, text ="Wyświetl obraz",                          command = self.option1_callback)
        option2 = Button(main_window, width = b_width, text ="Wypisz informacje o obrazie",             command = self.option2_callback)
        option3 = Button(main_window, width = b_width, text ="Wyświetl transformatę obrazu",            command = self.option3_callback)
        option4 = Button(main_window, width = b_width, text ="Zapisz obraz usuwając zbędne metadane",   command = self.option4_callback)
        option5 = Button(main_window, width = b_width, text ="Wyjdź",                                   command = self.option5_callback)
        
        option1.pack()
        option2.pack()
        option3.pack()
        option4.pack()
        option5.pack()

        main_window.mainloop()

    ############################################################################################

    def option1_callback(self):
        show.show_image(self.pic_inf.file_name)

    def option2_callback(self):
        parser.more_info_jpg(self.pic_inf)

    def option3_callback(self):
        fft1.fourier(self.pic_inf.file_name)

    def option4_callback(self):
        parser.save_jpg(self.pic_inf)

    def option5_callback(self):
        exit()