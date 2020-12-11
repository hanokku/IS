import random
import os
from math import sqrt


def euclid(a, b):
    while b != 0:
        a, b = b, a % b
    return a

   
def is_prime(num):
    for i in range(2, int(sqrt(num))):
        if (num % i == 0):
            return False
    return True


def find_e(phi):
    while True:
        n = random.randint(2, 255)
        if euclid(n, phi) == 1:
            return n


def find_d(e, phi):
    k = 0
    while ((k * phi + 1) % e != 0):
        k += 1
    return ((k * phi + 1) // e)


def get_keys(phi, n):
    public_key = (find_e(phi), n)
    private_key = (find_d(public_key[0], phi), n)
    return public_key, private_key


def encrypt_message(message, key):
    e, n = key
    return "".join([chr(ord(char) ** e % n) for char in message])


def decrypt_message(message, key):
    d, n = key
    return "".join([chr(ord(char) ** d % n) for char in message])


def encrypt_file(in_file, out_file, public_key):
    try:
        input_file = open(in_file, 'rb')
    except FileNotFoundError:
        print("No such file! Try again!")
        return

    output_file = open(out_file, 'w')
    data = input_file.read()
    input_file.close()
    bytes_to_write = ""

    for symbol in data:
        symbol = chr(symbol)
        bytes_to_write += encrypt_message(symbol, public_key)
    output_file.write(bytes_to_write)
    output_file.close()


def decrypt_file(in_file, out_file, private_key):
    try:
        input_file = open(in_file, 'r')
    except FileNotFoundError:
        print("No such file! Try again!")
        return

    output_file = open(out_file, 'wb')
    data = input_file.read()
    input_file.close()
    bytes_to_write = b""

    for symbol in data:
        symbol = decrypt_message(symbol, private_key)
        bytes_to_write += bytes([ord(symbol)])
    output_file.write(bytes_to_write)
    output_file.close()


def main():
    choice = None

    while choice != '0':
        choice = input('''
=======================================================
1. Input message from terminal and encrypt it.
2. Input message from file and encrypt it.
0. Exit.
Your choice: ''')
        print('=======================================================')

        if choice == '1':
            p = int(input("\nInput number p: "))
            q = int(input("Input number q: "))

            if not (is_prime(p) and is_prime(q)):
                raise ValueError('Both numbers must be prime!')
            elif p == q:
                raise ValueError('p and q can not be equal!')

            n = p * q

            if (n < 256):
                raise ValueError("Numbers' multiplication must be bigger than 256!")

            phi = (p - 1) * (q - 1)
            public_key, private_key = get_keys(phi, n)

            message = input("\nMessage to encrypt: ")
            encrypted = encrypt_message(message, public_key)
            decrypted = decrypt_message(encrypted, private_key)

            print("Your message before encryption: ", message)
            print("Your message after encryption: ", encrypted)
            print("Your message after decryptyion: ", decrypted)
    
        if choice == '2':
            p = int(input("\nInput number p: "))
            q = int(input("Input number q: "))

            if not (is_prime(p) and is_prime(q)):
                raise ValueError('Both numbers must be prime!')
            elif p == q:
                raise ValueError('p and q can not be equal!')

            n = p * q

            if (n < 256):
                raise ValueError("Numbers' multiplication must be bigger than 256!")

            phi = (p - 1) * (q - 1)
            public_key, private_key = get_keys(phi, n)
            
            input_file = input("\nInput name of reading file: ")
            filename = os.path.splitext(input_file)
            res_file = filename[0] + '_encrypt' + filename[1]

            encrypt_file(input_file, res_file, public_key)
            decrypt_file(res_file, filename[0] + '_decrypt' + filename[1], private_key)
    

if __name__ == '__main__':
    main()