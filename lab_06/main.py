import argparse
import struct
import sys
import os


# Создание парсера
def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f", "--file",
        required=True, type=str,
        help="source file"
    )
    return parser


# Узел
class Node():
    def __init__(self, value, frequency, parent=None, left=None, right=None):
        self.value = value
        self.frequency = frequency
        self.parent = parent
        self.left = left
        self.right = right
    
    def sort_by_frequency(node):
        return node.frequency


# Алгоритм Хаффмана
class HuffmanCoding():
    def __init__(self, input_file):
        self.table = self.make_frequency_table(input_file)
        self.codes = self.make_codes_table()

    # Таблица частот
    def make_frequency_table(self, filename):
        tbl = [0] * 256
        try:
            fl = open(filename, "rb")
        except FileNotFoundError:
            print("No such file! Try again!")
            return

        string = fl.read()
        fl.close()

        for char in string:
            tbl[char] += 1
        
        return tbl
        
    # Таблица кодов
    def make_codes_table(self):
        # Список свободных узлов
        nodes = []

        # Узлы нижнего уровня и таблица кодов
        leafs = []
        codes = []

        for i in range(len(self.table)):
            if self.table[i] > 0:
                nodes.append(Node(i, self.table[i]))
        
        if len(nodes) == 1:
            leafs.append(nodes[0])
            codes.append((nodes[0].value, "0"))
            return codes
        
        # Сортировка по неубыванию, поиск нового узла (сумма двух потомков)
        while len(nodes) > 1:
            nodes.sort(key = Node.sort_by_frequency)
            left, right = nodes.pop(0), nodes.pop(0)
            temp_node = Node(None, left.frequency + right.frequency, None, left, right)
            left.parent = temp_node
            right.parent = temp_node

            if(left.value != None):
                leafs.append(left)

            if(right.value != None):
                leafs.append(right)

            nodes.append(temp_node)

        # Таблица кодов
        for el in leafs:
            code = ""
            node = el

            while True:
                parent = node.parent

                if parent == None:
                    break
                if node == parent.left:
                    code = code + "0"
                if node == parent.right:
                    code = code + "1"
                node = parent
            codes.append((el.value, code[::-1]))
        
        return codes

    # перевести бит в байт
    def convert_bit_str_to_byte(self, string):
        return struct.pack("B", int(string, 2))

    # поиск кода по номеру ASCII в таблице кодов
    def find_code(self, num):
        for i in range(len(self.codes)):
            if self.codes[i][0] == num:
                return self.codes[i][1]
    
    # поиск байта при расшифровке в таблице кодов
    def find_byte(self, code):
        for i in range(len(self.codes)):
            if self.codes[i][1] == code:
                return self.codes[i][0]
        
        return None

    # сжатие файла
    def compress(self, input_file):
        codes_file = "code.txt"
        codes_fl = open(codes_file, "w")

        for item in self.codes:
            codes_fl.write("{} {}\n".format(item[0], item[1]))
        
        codes_fl.close()

        zrs = 0
        code_str = ""
        filename = os.path.splitext(input_file)
        res_file = filename[0] + '_compressed' + filename[1]

        try:
            input_fl = open(input_file, "rb")
        except FileNotFoundError:
            print("No such file! Try again!")
            return

        res_fl = open(res_file, "wb")

        string = input_fl.read()

        for char in string:
            code = self.find_code(char)
            code_str = code_str + code

            if len(code_str) >= 8:
                byte_str = code_str[:8]
                code_str = code_str[8:]
                byte = self.convert_bit_str_to_byte(byte_str)
                res_fl.write(byte)
        
        if len(code_str) > 0:
            zrs = 8 - len(code_str)

            for i in range(zrs):
                code_str += "0"
            byte = self.convert_bit_str_to_byte(code_str)
            res_fl.write(byte)
        
        input_fl.close()
        res_fl.close()

        return codes_file, res_file, zrs
    
    # восстановление файла
    def decompress(self, input_file, compressed_file, zrs):
        filename = os.path.splitext(input_file)
        res_file = filename[0] + '_decompressed' + filename[1]

        try:
            compressed_fl = open(compressed_file, "rb")
        except FileNotFoundError:
            print("No such file! Try again!")
            return

        res_fl = open(res_file, "wb")
        code_str = ""

        string = compressed_fl.read()

        for byte in string:
            code = bin(byte)[2:].zfill(8)
            code_str = code_str + code
        
        if zrs:
            code_str = code_str[:-zrs]
        
        code = ""

        while len(code_str):
            code = code + code_str[0]
            code_str = code_str[1:]
            byte = self.find_byte(code)

            if byte != None:
                res_fl.write(struct.pack("B", byte))
                code = ""
        
        compressed_fl.close()
        res_fl.close()

        return res_file
        

def main():
    parser = create_parser()
    args = parser.parse_args(sys.argv[1:])
    
    huffman = HuffmanCoding(args.file)
    codes_fl, res_fl, zrs = huffman.compress(args.file)
    decompress_fl = huffman.decompress(args.file, res_fl, zrs)

    print("Source file: '{}' ({} bytes)".format(args.file, os.path.getsize(args.file)))
    print("===============================================")
    print("Compressed file: '{}'  ({} bytes)".format(res_fl,  os.path.getsize(res_fl)))
    print("Codes table: {} bytes".format(sys.getsizeof(huffman.codes)))
    print("Decompressed file: '{}'  ({} bytes)".format(decompress_fl,  os.path.getsize(decompress_fl)))


if __name__ == '__main__':
    main()
    