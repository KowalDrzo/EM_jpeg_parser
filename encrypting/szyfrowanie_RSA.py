import random
from typing import List, Type
import sympy
from sympy.printing.codeprinter import print_fcode
from encrypting.chunk_editor import ChunkEditor

"""
OPIS TODO!!!
"""

class Encryptor:

    """
    Generowanie klucza publicznego i prywatnego
    """

    def generateKeys(self, key_size=1024):
        public_key = private_key = N = 0
        #N - iloczyn liczb pierwszych

        #generowanie 2 losowych liczb pierwszych
        p = sympy.randprime(2 ** (key_size - 1), 2 ** key_size - 1) 
        q = sympy.randprime(2 ** (key_size - 1), 2 ** key_size - 1)

        N = p * q 
        totient = (p - 1) * (q - 1) #obliczanie tocjentu

        while True: 
            public_key = random.randrange(2 ** (key_size - 1), 2 ** key_size - 1) #losowanie klucza publicznego
            if (self.isCoPrime(public_key, totient)): #sprawdzanie klucz publiczny jest względnie pierwszy z tocjentem
                break

        private_key = self.modular_inverse(public_key, totient) #generowanie klucza przywatnego, przy pomocy odwrotności modularnej
    

        return public_key, private_key, N 

    ################################################################

    """
    funkcja sprawdzająca czy podane jej argumenty są względnie pierwsze, jeśli tak zwraca True
    """

    def isCoPrime(self, p, q):

        return self.gcd(p, q) == 1

    ################################################################

    """
    algorytm Euklidesa, znajduje największy wspólny dzielnik p i q
    """

    def gcd(self, p, q):

        while q:
            p, q = q, p % q
        return p

    ################################################################

    """
    rozszerzony algorytm Euklidesa
    """

    def egcd(self, a, b):
        s = 0; old_s = 1
        t = 1; old_t = 0
        r = b; old_r = a 

        while r != 0:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t

        return old_r, old_s, old_t

    ################################################################

    """
    OPIS TODO!!!
    """

    def modular_inverse(self, a, b): 

        gcd, x, y = self.egcd(a, b)
        

        if x < 0: ##jeżeli x (klucz prywatny) będzie mniejsze od 0 to dodajemy do niego tocjent
            x += b

        return x

    ################################################################
    ################################################################
    ################################################################

    def encrypt(self, public_key, N, bin_file) -> List[bytes]:
        
        new_parts = []
        new_val = 0
        parts_8_bytes = list(self.divide_blocks(bin_file, 128))
        last_block_size = len(bin_file) % 128

        print("Szyfruję RSA")

        for part in parts_8_bytes:

            c = int.from_bytes(part, byteorder="big")
            new_val = pow(c, public_key, N)
            new_parts += new_val.to_bytes(256, "big")

        new_parts.insert(0, last_block_size)
        print(new_parts[0])
        print("Koniec RSA")

        return new_parts

    ################################################################

    def divide_blocks(self, l, n) -> List:
        
        new_list = []
        for i in range(0, len(l), n):
            new_list.append(l[i:i + n])

        return new_list

    ################################################################

    def decrypt(self, private_key, N, bin_file) -> List[bytes]: 
        
        original_file = []
        last_block_size = bin_file.pop(0)
        print(last_block_size)
        parts_8_bytes = list(self.divide_blocks(bin_file, 128))
        new_val = 0

        print("Deszyfruję RSA")

        for part in parts_8_bytes:

            c = int.from_bytes(part, byteorder="big")

            new_val = pow(c, private_key, N)
            if part is parts_8_bytes[-1]:
                original_file += new_val.to_bytes(256, "big")
                print("Koniec RSA")
            else:
                original_file += new_val.to_bytes(256, "big")

        return original_file

    ################################################################
    ################################################################
    ################################################################

    def showGeneratedKeys(self) -> List[str]:
        
        public_key, private_key, N = self.generateKeys()
        retList = []

        print("\nNowy klucz publiczny:")
        print(public_key)
        print("\nNowy klucz prywatny:")
        print(private_key)
        print("\nNowy modulator:")
        print(N)

        retList.append(str(N))
        retList.append(str(public_key))

        return retList

    ################################################################

    def save_encrypted(self, pic_inf, new_name, key: int, N: int, decryption: bool, encrypt_tabs: bool):
        
        new_file = open(new_name, "wb")

        # Początek pliku:
        new_file.write(bytes([0xff, 0xd8]))

        # Zapis niezmienionyh metadanych:
        for meta_chunk in pic_inf.metadata_chunks:
            new_file.write(bytes([0xff, meta_chunk.marker]))
            new_file.write(bytes(pic_inf.binary_file[meta_chunk.begin_ind:meta_chunk.end_ind]))

        # Zapis zmienionych danych właściwych:
        for nec_chunk in pic_inf.necessary_chunks:
            
            new_file.write(bytes([0xff, nec_chunk.marker]))
            if nec_chunk.marker == 0xda:
                
                new_file.write(bytes(pic_inf.binary_file[nec_chunk.begin_ind:nec_chunk.begin_ind + nec_chunk.header_len]))
                
                if not decryption:
                    enc = self.encrypt(key, N, pic_inf.binary_file[nec_chunk.begin_ind + nec_chunk.header_len:nec_chunk.end_ind])
                    sof_edited = ChunkEditor.edit_for_sof(enc, decryption)
                
                else:
                    sof_edited = ChunkEditor.edit_for_sof(pic_inf.binary_file[nec_chunk.begin_ind + nec_chunk.header_len:nec_chunk.end_ind], decryption)
                    enc = self.decrypt(key, N, sof_edited)
                
                new_file.write(bytes(sof_edited))

            elif encrypt_tabs and (nec_chunk.marker == 0xdb or nec_chunk.marker == 0xc4):

                    enc = self.encrypt(key, N, pic_inf.binary_file[nec_chunk.begin_ind+2:nec_chunk.end_ind])
                    new_len = ChunkEditor.edit_for_tabs(enc)
                    new_file.write(bytes(new_len))
                    new_file.write(bytes(enc))
            
            else: 
                new_file.write(bytes(pic_inf.binary_file[nec_chunk.begin_ind:nec_chunk.end_ind]))

        # Koniec pliku:
        new_file.write(bytes([0xff, 0xd9]))

        new_file.close()