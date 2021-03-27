#szybka transformata Fouriera
import cv2
import numpy as np
#import glob

img = cv2.imread("led1.jpg", cv2.IMREAD_GRAYSCALE)

f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20 * np.log(np.abs(fshift))
magnitude_spectrum = np.asarray(magnitude_spectrum, dtype = np.uint8)
cv2.imshow("Magnitude spectrum", magnitude_spectrum)
cv2.imshow("Image", img)

cv2.waitKey(0)
cv2.destroyAllWindows()