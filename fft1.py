import cv2
import numpy as np

"""
Funkcja fourier przeznaczona do realizowania obliczenia i wyświetlenia transformaty fouriera z obrazu

Parametry:
    file_name - nazwa pliku.
"""

def fourier(file_name):
    
    img = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)

    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)

    # liczenie modułu
    magnitude_spectrum = 20 * np.log(np.abs(fshift))
    magnitude_spectrum = np.asarray(magnitude_spectrum, dtype = np.uint8)

    # liczenie fazy
    phase_spectrum = np.angle(fshift)
    phase_spectrum = np.asarray(phase_spectrum, dtype = np.uint8)

    # wyświetlanie
    cv2.imshow("Obraz w odcieniach szarosci", img)
    cv2.imshow("Faza widma", phase_spectrum)
    cv2.imshow("Modul widma", magnitude_spectrum)

    cv2.waitKey(0)
    cv2.destroyAllWindows()