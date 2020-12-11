import random
import os


ARR_LENGTH = 256


# инициализация ротора
def init_rotor():
    rotor = [None for _ in range(ARR_LENGTH)]
    num = 0

    while None in rotor:
        ind = random.randint(0, ARR_LENGTH - 1)
        if rotor[ind] == None:
            rotor[ind] = num
            num += 1
    
    return rotor


# инициализация рефлектора
def init_reflector():
    reflector = [None for _ in range(ARR_LENGTH)]
    arr = [x for x in range(ARR_LENGTH)]

    for i in range(ARR_LENGTH):
        if reflector[i] == None:
            num = random.choice(arr)
            while num == i:
                num = random.choice(arr)
            arr.pop(arr.index(num))
            arr.pop(arr.index(i))
            reflector[i] = num
            reflector[num] = i
            
    return reflector


# шифрование символа
def encrypt_symbol(s, first_rotor, second_rotor, third_rotor, reflector):
    # for i in range(len(first_rotor)):
        # print(reflector[i], '     ', third_rotor[i], '     ', second_rotor[i], '     ', first_rotor[i])
    s1 = first_rotor.index(s)
    s2 = second_rotor.index(s1)
    s3 = third_rotor.index(s2)
    s4 = reflector.index(s3)
    s5 = third_rotor[s4]
    s6 = second_rotor[s5]
    s7 = first_rotor[s6]
    # print(s1, s2, s3, s4, s5, s6, s7)
    # print(reflector)
    return s7


# проворачиваем роторы и шифруем сообщение
def encrypt_message(msg, first_rotor, second_rotor, third_rotor, reflector):
    nums = [ord(c) for c in msg]
    res_msg = []
    shift1 = 0
    shift2 = 0
    shift3 = 0
    for s in nums:
        res_msg.append(encrypt_symbol(s, first_rotor, second_rotor, third_rotor, reflector))
        if shift1 < ARR_LENGTH:
            first_rotor = first_rotor[1:] + first_rotor[:1]
            shift1 += 1
        elif shift2 < ARR_LENGTH:
            first_rotor = first_rotor[1:] + first_rotor[:1]
            second_rotor = second_rotor[1:] + second_rotor[:1]
            shift1 = 0
            shift2 += 1
        elif shift3 < ARR_LENGTH:
            first_rotor = first_rotor[1:] + first_rotor[:1]
            second_rotor = second_rotor[1:] + second_rotor[:1]
            third_rotor = third_rotor[1:] + third_rotor[:1]
            shift1 = 0
            shift2 = 0
            shift3 += 1
        else:
            first_rotor = first_rotor[1:] + first_rotor[:1]
            second_rotor = second_rotor[1:] + second_rotor[:1]
            third_rotor = third_rotor[1:] + third_rotor[:1]
            shift1 = 0
            shift2 = 0
            shift3 = 0

    return ''.join([chr(c) for c in res_msg])


# шифруем/расшифровываем файл
def encrypt_file(in_file, out_file, first_rotor, second_rotor, third_rotor, reflector):
    try:
        input_file = open(in_file, 'rb')
    except FileNotFoundError:
        print("No such file! Try again!")
        return

    output_file = open(out_file, 'wb')
    read_byte = input_file.read(1000)

    while read_byte:
        byte_encrypt = b""
        for s in read_byte:
            ch = chr(s)
            ch = encrypt_message(ch, first_rotor, second_rotor, third_rotor, reflector)
            byte_encrypt += bytes([ord(ch)])
        output_file.write(byte_encrypt)
        read_byte = input_file.read(1000)

    input_file.close()
    output_file.close()


def main():
    first_rotor = init_rotor()
    second_rotor = init_rotor()
    third_rotor = init_rotor()
    reflector = init_reflector()

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
            msg = input("\nMessage to encrypt: ")
            msg_encrypt = encrypt_message(msg, first_rotor, second_rotor, third_rotor, reflector)
            msg_decrypt = encrypt_message(msg_encrypt, first_rotor, second_rotor, third_rotor, reflector)

            print("Your message before encryption: ", msg)
            print("Your message after encryption: ", msg_encrypt)
            print("Your message after decryptyion: ", msg_decrypt)
        elif choice == '2':
            input_file = input("\nInput name of reading file: ")
            filename = os.path.splitext(input_file)
            res_file = filename[0] + '_encrypt' + filename[1]

            encrypt_file(input_file, res_file, first_rotor, second_rotor, third_rotor, reflector)
            encrypt_file(res_file, filename[0] + '_decrypt' + filename[1], first_rotor, second_rotor, third_rotor, reflector)
        elif choice == '3':
            input_file = '123.jpg'
            filename = os.path.splitext(input_file)
            res_file = filename[0] + '_encrypt' + filename[1]

            encrypt_file(input_file, res_file, first_rotor, second_rotor, third_rotor, reflector)
            encrypt_file(res_file, filename[0] + '_decrypt' + filename[1], first_rotor, second_rotor, third_rotor, reflector)
            os.system("open " + "123_decrypt.jpg")
    
if __name__ == '__main__':
    main()
