from PIL import Image
from encrypting.szyfrowanie_RSA import Encryptor


def encrypt_not_compressed(file_name, new_file_name, key, N_val):

    im = Image.open(file_name)

    pixels = list(im.getdata())
    width, height = im.size
    new_pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

    encryptor = Encryptor()

    new_pixels = encryptor.encrypt(key, N_val, new_pixels)

    im.save(new_file_name)