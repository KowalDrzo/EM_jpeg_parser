import random
from typing import List, Type
import sympy
from sympy.printing.codeprinter import print_fcode

class Encryptor:

    end_block_size = 0
    
    public_key = 0
    private_key = 0
    N = 0

    def rabinMiller(self, n, private_key):
        a = random.randint(2, (n - 2) - 2)
        x = pow(a, int(private_key), n) # a^private_key%n
        if x == 1 or x == n - 1:
            return True

        # square x
        while private_key != n - 1:
            x = pow(x, 2, n)
            private_key *= 2

            if x == 1:
                return False
            elif x == n - 1:
                return True
        
        # is not prime
        return False

    def isPrime(self, n): #zwraca True jeśli liczba jest pierwsza, test Rabina-Millera jeśli jest niepewna
        
        return sympy.isprime(n)

    def generateKeys(self, keysize=1024):
        public_key = private_key = N = 0

        # generowanie 2 losowych liczb pierwszych
        p = self.generateLargePrime(keysize) #wygenerowana liczba pierwsza
        q = self.generateLargePrime(keysize) #druga wygenerowana liczba pierwsza

        #print(f"p: {p}")
        #print(f"q: {q}")

        N = p * q #iloczyn liczb pierwszych
        totient = (p - 1) * (q - 1) # totient

        # choose public_key
        # public_key jest względnie pierwsze z totientem & 1 < public_key <= totient
        while True:
            public_key = random.randrange(2 ** (keysize - 1), 2 ** keysize - 1) #klucz publiczny
            if (self.isCoPrime(public_key, totient)): #sprawdzenie czy public_key jest względnie pierwsza z tocjentem
                break

        # wybór private_key
        # private_key jest odwrotnością modularną public_key z totientem, public_key * private_key (mod totient) = 1
        private_key = self.modular_inverse(public_key, totient) #klucz prywatny

        return public_key, private_key, N

    def generateLargePrime(self, keysize):
        """
            return random large prime number of keysize bits in size
        """

        return sympy.randprime(2 ** (keysize - 1), 2 ** keysize - 1)


    def isCoPrime(self, p, q):
        """
            return True if gcd(p, q) is 1
            relatively prime
        """

        return self.gcd(p, q) == 1

    def gcd(self, p, q):
        """
            euclidean algorithm to find gcd of p and q
        """

        while q:
            p, q = q, p % q
        return p

    def egcd(self, a, b):
        s = 0; old_s = 1
        t = 1; old_t = 0
        r = b; old_r = a

        while r != 0:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t

        # return gcd, x, y
        return old_r, old_s, old_t

    def modular_inverse(self, a, b): #generuje 
        gcd, x, y = self.egcd(a, b)

        if x < 0:
            x += b

        return x

    ################################################################
    ################################################################
    ################################################################

    def encrypt(self, public_key, N, bin_file) -> List[bytes]:
        
        new_parts = []
        new_val = 0
        parts_8_bytes = list(self.divide_blocks(bin_file, 4))

        print(str(len(bin_file) % 4))

        for part in parts_8_bytes:

            c = int.from_bytes(part, byteorder="big")
            new_val = pow(c, public_key, N)

            print(str(new_val % 4))

            if part is parts_8_bytes[-1]:

                print("dl: " + str(len(part)))
                new_parts += new_val.to_bytes(4, "big")
                print("ostatni")
            else:
                new_parts += new_val.to_bytes(4, "big")

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
        parts_8_bytes = list(self.divide_blocks(bin_file, 4))
        new_val = 0

        for part in parts_8_bytes:

            c = int.from_bytes(part, byteorder="big")

            print(str(c % 4))

            new_val = pow(c, private_key, N)
            if part is parts_8_bytes[-1]:
                original_file += new_val.to_bytes(4, "big")
                print("ostatni")
            else:
                original_file += new_val.to_bytes(4, "big")

        return original_file

    ################################################################
    ################################################################
    ################################################################

    def showGeneratedKeys(self):
        
        self.public_key, self.private_key, self.N = self.generateKeys()
        
        print("\nNowy klucz publiczny:")
        print(self.public_key)
        print("\nNowy klucz prywatny:")
        print(self.private_key)
        print("\nNowy modulator:")
        print(self.N)

    ################################################################

    def save_encrypted(self, pic_inf, newfile_name):
        i = 5
        i += 1

    ################################################################

    def save_decrypted(self, pic_inf):
        pass

"""
keysize = 16

public_key, private_key, N = generateKeys(keysize)

print("Wczytuję")

file = open("Patyczak.jpg", "rb")
bin_file = list(file.read())
file.close()

print("Szyfruję")

enc = encrypt(public_key, N, bin_file)

print("Zapisuję")

file = open("SFR.jpg", "wb")
file.write(bytes(enc))
file.close()

print("Odszyfrowywuję")

file = open("SFR.jpg", "rb")
bin_file = list(file.read())
file.close()

dec = decrypt(private_key, N, bin_file)

print("Zapisuję odszyfrowany")

file = open("SFR2.jpg", "wb")
file.write(bytes(dec))
file.close()
"""