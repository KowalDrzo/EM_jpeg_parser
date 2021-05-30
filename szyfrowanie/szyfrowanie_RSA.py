import random
from typing import Type
import sympy
from sympy.printing.codeprinter import print_fcode

def rabinMiller(n, private_key):
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

def isPrime(n): #zwraca True jeśli liczba jest pierwsza, test Rabina-Millera jeśli jest niepewna
    
    return sympy.isprime(n)

    """
    # 0, 1, -ve numbers not prime
    if n < 2:
        return False

    # low prime numbers to save time
    lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

    # if in lowPrimes
    if n in lowPrimes:
        return True

    # if low primes divide into n
    for prime in lowPrimes:
        if n % prime == 0:
            return False
    
    # find number c such that c * 2 ^ r = n - 1
    c = n - 1 # c even bc n not divisible by 2
    while c % 2 == 0:
        c /= 2 # make c odd

    # prove not prime 128 times
    for i in range(128):
        if not rabinMiller(n, c):
            return False

    return True
    """

def generateKeys(keysize=1024):
    public_key = private_key = N = 0

    # generowanie 2 losowych liczb pierwszych
    p = generateLargePrime(keysize) #wygenerowana liczba pierwsza
    q = generateLargePrime(keysize) #druga wygenerowana liczba pierwsza

    print(f"p: {p}")
    print(f"q: {q}")

    N = p * q #iloczyn liczb pierwszych
    totient = (p - 1) * (q - 1) # totient

    # choose public_key
    # public_key jest względnie pierwsze z totientem & 1 < public_key <= totient
    while True:
        public_key = random.randrange(2 ** (keysize - 1), 2 ** keysize - 1) #klucz publiczny
        if (isCoPrime(public_key, totient)): #sprawdzenie czy public_key jest względnie pierwsza z tocjentem
            break

    # wybór private_key
    # private_key jest odwrotnością modularną public_key z totientem, public_key * private_key (mod totient) = 1
    private_key = modular_inverse(public_key, totient) #klucz prywatny

    return public_key, private_key, N

def generateLargePrime(keysize):
    """
        return random large prime number of keysize bits in size
    """

    return sympy.randprime(2 ** (keysize - 1), 2 ** keysize - 1)


def isCoPrime(p, q):
    """
        return True if gcd(p, q) is 1
        relatively prime
    """

    return gcd(p, q) == 1

def gcd(p, q):
    """
        euclidean algorithm to find gcd of p and q
    """

    while q:
        p, q = q, p % q
    return p

def egcd(a, b):
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

def modular_inverse(a, b): #generuje 
    gcd, x, y = egcd(a, b)

    if x < 0:
        x += b

    return x

def encrypt(public_key, N, bin_file):
    
    new_file = []
    new_val = 0

    for byte in bin_file:

        new_val = pow(byte, public_key, N)
        new_file.append(new_val.to_bytes(8, "big"))

    return new_file

def divide_chunks(l, n):
      
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]

def decrypt(private_key, N, bin_file):
    
    original_file = []
    parts_8_bytes = divide_chunks(bin_file, 8)

    #parts = cipher.split()
    for part in parts_8_bytes:
        c = int.from_bytes(part, byteorder="big")
        original_file.append(pow(c, private_key, N))

    return original_file


keysize = 16

public_key, private_key, N = generateKeys(keysize)

print("Wczytuję")

file = open("../Obraz/Patyczak.jpg", "rb")
bin_file = list(file.read())
file.close()

print("Szyfruję")

enc = encrypt(public_key, N, bin_file)

print("Zapisuję")

file = open("SFR.jpg", "wb")

for byte in enc:
    file.write(byte)
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