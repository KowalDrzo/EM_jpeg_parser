from PIL import Image
from encrypting.szyfrowanie_RSA import Encryptor


def encrypt_not_compressed(file_name, new_file_name, key, N_val):

    im = Image.open(file_name)

    pixels_r = []
    pixels_g = []
    pixels_b = []

    print("Przekształcam plik na pixele")
    for i in range(im.size[0]):
        for j in range(im.size[1]):

            (r, g, b) = im.getpixel((i, j))
            pixels_r.append(r)
            pixels_g.append(g)
            pixels_b.append(b)
    
    encryptor = Encryptor()

    print("R")
    pixels_r = encryptor.encrypt(key, N_val, pixels_r)
    print("G")
    pixels_g = encryptor.encrypt(key, N_val, pixels_g)
    print("B")
    pixels_b = encryptor.encrypt(key, N_val, pixels_b)

    print("zapis")
    for i in range(im.size[0]):
        for j in range(im.size[1]):

            place = im.size[0] * i + j
            im.putpixel((i, j), (pixels_r[place], pixels_g[place], pixels_b[place]))

    im.save(new_file_name)
    print("koniec")