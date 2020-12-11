from tables import *
from bitarray import bitarray
import os

ROUND_CNT = 16
MSG_LEN = 64

# чтение ключа из файла
def read_key():
    file_key = open('key.txt', 'r')
    key = file_key.read()
    file_key.close()

    return bitarray(str(key))

# побитовый сдвиг для ключа
def shift_left(msg_bitarray):
    return msg_bitarray[1:] + bitarray(str(int(msg_bitarray[0])))

# перестановка
def replace_by_table(msg_bitarray, table_list):
    res_bitarray = bitarray()

    for i in range(len(table_list)):
        res_bitarray.append(msg_bitarray[table_list[i] - 1])
    
    return res_bitarray

# перестановка в S-блоках
def S_shift(msg_bitarray, S_matrix):
    msg_bitarray_str = str(msg_bitarray.to01())
    line = int(msg_bitarray_str[0] + msg_bitarray_str[-1], base = 2)
    column = int(msg_bitarray_str[1:-1], base = 2)
    res_bitarray = bitarray(bin(S_matrix[line][column])[2:])

    while len(res_bitarray) < 4:
        res_bitarray = bitarray('0') + res_bitarray

    return res_bitarray

# функция Фейстеля
def function_feistel(msg_bitarray, key):
    msg_bitarray = replace_by_table(msg_bitarray, E)
    msg_bitarray = msg_bitarray ^ key

    res_bitarray = bitarray()

    for i in range(8):
        res_bitarray += S_shift(msg_bitarray[(i*6):((i+1)*6)], S[i])
    
    res_bitarray = replace_by_table(res_bitarray, P)
    return res_bitarray

# генерация раундовых ключей
def key_generation_round(key_bitarray):
    key_bitarray = replace_by_table(key_bitarray, G)
    C = key_bitarray[:28]
    D = key_bitarray[28:]

    keys_arr = []

    for i in range(ROUND_CNT):
        for j in range(Si_shift[i]):
            C = shift_left(C)
            D = shift_left(D)
        new_key = replace_by_table(C + D, H)
        keys_arr.append(new_key)
    
    return keys_arr

# алгоритм шифрования
def __DES(msg_bitarray, key, decode):
    msg_bitarray = replace_by_table(msg_bitarray, IP)

    keys_arr = key_generation_round(key)
    
    if decode:
        keys_arr.reverse()

    L_old = L = msg_bitarray[:MSG_LEN//2]
    R_old = R = msg_bitarray[MSG_LEN//2:]

    for i in range(ROUND_CNT):
        if not decode:
            L = R
            R = L_old ^ function_feistel(R, keys_arr[i])
            L_old = L
        else:
            R = L
            L = R_old ^ function_feistel(L, keys_arr[i])
            R_old = R

    msg_bitarray = replace_by_table(L + R, IP_rev)
    return msg_bitarray

# обертка алгоритма
def des_algorithm(msg_bitarray, key, decode = False):
    num = 0
    while len(msg_bitarray) % MSG_LEN != 0:
        msg_bitarray += bitarray('0')
        num += 1

    res_bitarray = bitarray()
    for i in range(len(msg_bitarray) // MSG_LEN):
        res_bitarray += __DES(msg_bitarray[i * MSG_LEN : (i+1) * MSG_LEN], key, decode)

    return res_bitarray, num

# шифрование файла
def encrypt_file(in_file, out_file, decode = False):
    try:
        input_file = open(in_file, 'rb')
    except FileNotFoundError:
        print("No such file! Try again!")
        return

    msg_bitarray = bitarray()
    input_file = open(in_file, 'rb')
    msg_bitarray.fromfile(input_file)
    input_file.close()

    res_bitarray, _ = des_algorithm(msg_bitarray, key, decode)

    output_file = open(out_file, 'wb')
    res_bitarray.tofile(output_file)
    output_file.close()


if __name__ == '__main__':
    key = read_key()

    choice = None

    while choice != '0':
        choice = input('''
=======================================================
1. Input message from terminal and encrypt it.
2. Input message from file and encrypt it.
3. Зашифровать картиночку с котеком!
0. Exit.
Your choice: ''')
        print('=======================================================')

        if choice == '1':
            message = input("\nMessage to encrypt: ")
            
            message_bitarray = bitarray()
            message_bitarray.frombytes(message.encode('utf-8'))

            res_bitarray, num_enc = des_algorithm(message_bitarray, key)
            decoded_msg, num_dec = des_algorithm(res_bitarray, key, True)
            decoded_msg = decoded_msg[0:len(decoded_msg) - num_enc]

            print("Your message before encryption: ", message)
            print("Your message after encryption: ", bytearray(bitarray(res_bitarray).tobytes()).hex().upper())
            print("Your message after decryptyion: ", str(bitarray(decoded_msg).tobytes().decode()))
    
        if choice == '2':
            input_file = input("\nInput name of reading file: ")
            filename = os.path.splitext(input_file)
            res_file = filename[0] + '_encrypt' + filename[1]

            encrypt_file(input_file, res_file)
            encrypt_file(res_file, filename[0] + '_decrypt' + filename[1], True)
            
        if choice == '3':
            input_file = "test/cat.jpg"
            filename = os.path.splitext(input_file)
            res_file = filename[0] + '_encrypt' + filename[1]

            encrypt_file(input_file, res_file)
            encrypt_file(res_file, filename[0] + '_decrypt' + filename[1], True)
            os.system("open " + "test/cat_decrypt.jpg")