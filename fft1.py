#szybka transformata Fouriera
import cv2
import numpy as np
#import glob

img = cv2.imread("Obraz/led1.jpg", cv2.IMREAD_GRAYSCALE)

f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)

# liczenie modułu
magnitude_spectrum = 20 * np.log(np.abs(fshift))
magnitude_spectrum = np.asarray(magnitude_spectrum, dtype = np.uint8)

# liczenie modufazy
phase_spectrum = np.angle(fshift)
phase_spectrum = np.asarray(phase_spectrum, dtype = np.uint8)

# wyświetlanie
cv2.imshow("Obraz", img)
cv2.imshow("Faza widma", phase_spectrum)
cv2.imshow("Modul widma", magnitude_spectrum)

cv2.waitKey(0)
cv2.destroyAllWindows()