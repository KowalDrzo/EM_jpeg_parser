import random
from typing import List, Final
import sympy
from sympy.printing.codeprinter import print_fcode
from encrypting.chunk_editor import ChunkEditor

"""
Klasa Encryptor posiada wszelkie metody generowania klucza oraz przeprowadzenia szyfrowania i deszyfrowania.
"""

class Encryptor:

    PQ_SIZE : Final = 512
    WRITE_SIZE : Final = int(PQ_SIZE / 4)
    BLOCK_SIZE : Final = int(WRITE_SIZE / 2)

    """
    Generowanie klucza publicznego i prywatnego
    """

    def generateKeys(self):
        public_key = private_key = N = 0
        #N - iloczyn liczb pierwszych

        #generowanie 2 losowych liczb pierwszych
        p = sympy.randprime(2 ** (self.PQ_SIZE - 1), 2 ** self.PQ_SIZE - 1) 
        q = sympy.randprime(2 ** (self.PQ_SIZE - 1), 2 ** self.PQ_SIZE - 1)

        N = p * q 
        totient = (p - 1) * (q - 1) #obliczanie tocjentu

        while True: 
            public_key = random.randrange(2 ** (self.PQ_SIZE - 1), 2 ** self.PQ_SIZE - 1) #losowanie klucza publicznego
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

    """
    Metoda szyfrująca.
    """

    def encrypt(self, public_key, N, bin_file) -> List[bytes]:
        
        new_parts = []
        new_val = 0
        blocks = list(self.divide_blocks(bin_file, self.BLOCK_SIZE))
        last_block_size = len(bin_file) % self.BLOCK_SIZE

        for part in blocks:

            c = int.from_bytes(part, byteorder="big")
            new_val = pow(c, public_key, N)
            new_parts += new_val.to_bytes(self.WRITE_SIZE, "big")

        new_parts.insert(0, last_block_size)

        return new_parts

    ################################################################

    """
    Metoda dzieląca listę bajtów na bloki.
    """

    def divide_blocks(self, l, n) -> List:
        
        new_list = []
        for i in range(0, len(l), n):
            new_list.append(l[i:i + n])

        return new_list

    ################################################################

    """
    Metoda deszyfrująca.
    """

    def decrypt(self, private_key, N, bin_file) -> List[bytes]: 
        
        original_file = []
        last_block_size = bin_file.pop(0)

        blocks = list(self.divide_blocks(bin_file, self.WRITE_SIZE))
        new_val = 0

        for part in blocks:

            c = int.from_bytes(part, byteorder="big")

            new_val = pow(c, private_key, N)
            if part is blocks[-1]:
                original_file += new_val.to_bytes(last_block_size, "big")
            else:
                original_file += new_val.to_bytes(self.BLOCK_SIZE, "big")

        return original_file

    ################################################################
    ################################################################
    ################################################################

    """
    Metoda wyświetlająca klucze.
    """

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

    """
    Metoda przeprowadzająca cały proces szyfrowania i deszyfrowania.
    """

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
            
            #####################################################################################
            # Dane obrazu za Sos:
            new_file.write(bytes([0xff, nec_chunk.marker]))
            if nec_chunk.marker == 0xda:
                
                new_file.write(bytes(pic_inf.binary_file[nec_chunk.begin_ind:nec_chunk.begin_ind + nec_chunk.header_len]))
                
                if not decryption:
                    enc = self.encrypt(key, N, pic_inf.binary_file[nec_chunk.begin_ind + nec_chunk.header_len:nec_chunk.end_ind])
                    sof_edited = ChunkEditor.edit_for_sof(enc, decryption)
                
                else:
                    sof_edited = ChunkEditor.edit_for_sof(pic_inf.binary_file[nec_chunk.begin_ind + nec_chunk.header_len:nec_chunk.end_ind], decryption)
                    enc = self.decrypt(key, N, sof_edited)
                
                new_file.write(bytes(enc))


            #####################################################################################
            # Tabele kwantyzacji i Huffmanna:

            elif encrypt_tabs and (nec_chunk.marker == 0xdb or nec_chunk.marker == 0xc4):

                if not decryption:
                
                    enc_or_dec = self.encrypt(key, N, pic_inf.binary_file[nec_chunk.begin_ind+2:nec_chunk.end_ind])

                else:

                    enc_or_dec = self.decrypt(key, N, pic_inf.binary_file[nec_chunk.begin_ind+2:nec_chunk.end_ind])

                new_len = ChunkEditor.edit_for_tabs(enc_or_dec)
                new_file.write(bytes(new_len))
                new_file.write(bytes(enc_or_dec))
            
            else: 
                new_file.write(bytes(pic_inf.binary_file[nec_chunk.begin_ind:nec_chunk.end_ind]))

        # Koniec pliku:
        new_file.write(bytes([0xff, 0xd9]))
        print("RSA zakończone")

        new_file.close()