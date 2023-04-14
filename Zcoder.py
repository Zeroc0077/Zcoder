# -*- encoding: utf-8 -*-
'''
@File    :   Zcoder.py
@Time    :   2023/04/08 14:25:35
@Author  :   zeroc 
'''
import sys
sys.dont_write_bytecode = True
from tqdm import tqdm
from math import log
from LZ import *
from Huffman import *
import os

def replace_last(string, old_substring, new_substring):
    head, sep, tail = string.rpartition(old_substring)
    if sep:
        return head + new_substring + tail
    else:
        return string


class Zcoder:
    # initialize the Zcoder
    def __init__(self, path: str) -> None:
        """
        Arguments:
        - path: str, the relative path of the file
        """
        path = os.path.abspath(__file__)[:-9] + path
        self.path = path  # absolute path of the file
        self.filecontent = open(self.path, "rb").read()  # content of the file
        self.dic = []  # the dictionary of the LZ coding
        # check if the file is empty
        if self.filecontent == b'':
            print("\033[0;31m [Error]The file is empty!\033[0m")
            exit(0)

    # compress the file using Huffman coding
    def Huffman_compress(self, output_path: str = None) -> None:
        # check if the file is already compressed with my file format
        File_Head = b"ZCHM"

        # make the frequency dictionary
        frequency = HuffmanCoding._MakeFrequencyDict(self.filecontent)

        # construct the codebook
        codebook = HuffmanCoding._ConstructCodeBook(frequency)
        codebook = HuffmanCoding.Canonical(codebook)
        # store the codebook with the canonical code
        max_length = 0
        for char in codebook:
            # ! calculate the max length of the codeword
            max_length = max(max_length, len(codebook[char]))
        length = [0 for _ in range(max_length + 1)]
        for char in codebook:
            # ! calculate the number of codewords with the same length
            length[len(codebook[char])] += 1
        #! if all the codewords have the same length, using 0 to sign it
        if length[max_length] == 256:
            length[max_length] = 0
        length.pop(0)  # remove the element whose length is 0
        length_data = bytes(length)
        code_data = b"".join(codebook.keys())
        codebook_data = bytes([max_length]) + length_data + code_data

        # encode the file
        encoded_data, padding = HuffmanCoding.Encode(
            self.filecontent, codebook)
        # write the encoded file
        if output_path:
            with open(output_path, "wb") as f:
                f.write(File_Head + codebook_data +
                        encoded_data + bytes([padding]))
                print("\033[0;32m [Success]Compress successfully!\033[0m")
                print("\033[0;32m [Success]The file is stored in {path}\033[0m".format(
                    path=output_path))
        else:
            with open(self.path + ".enc", "wb") as f:
                f.write(File_Head + codebook_data +
                        encoded_data + bytes([padding]))
                print("\033[0;32m [Success]Compress successfully!\033[0m")
                print("\033[0;32m [Success]The file is stored in {path}\033[0m".format(
                    path=self.path + ".enc"))

    # decompress the file using Huffman coding
    def Huffman_decompress(self, output_path: str = None) -> None:
        # check if the file is already compressed with my file format
        File_Head = b"ZCHM"

        # read the encoded file
        encoded_data = self.filecontent

        # check if the file is already compressed with my file format
        if encoded_data[:4] != File_Head:
            print(
                "\033[0;31m [Error]The file is not compressed with my algorithm\033[0m")
            exit(0)
        encoded_data = encoded_data[4:]

        # Recover the codebook
        max_length = int(encoded_data[0])
        length = list(encoded_data[1:max_length + 1])
        num = sum(length)
        if num == 0 and max_length != 0:
            num = 256
            length[max_length - 1] = 256
        value, length2 = [], []
        for i in range(1 + max_length, 1 + max_length + num):
            value.append(encoded_data[i])
        for i in range(max_length):
            length2 += [i + 1] * length[i]
        codebook = HuffmanCoding._ReConstruct(value, length2)

        # decode the file
        padding = encoded_data[-1]
        encoded_data = encoded_data[max_length + 1 + num:-1]
        decoded_data = HuffmanCoding.Decode(encoded_data, padding, codebook)
        # write the decoded file
        if output_path:
            with open(output_path, "wb") as f:
                f.write(decoded_data)
            print("\033[0;32m [Success]Decompress successfully!\033[0m")
            print("\033[0;32m [Success]The file is stored in {path}\033[0m".format(
                path=output_path))
        else:
            with open(replace_last(self.path, ".enc", ".dec"), "wb") as f:
                f.write(decoded_data)
            print("\033[0;32m [Success]Decompress successfully!\033[0m")
            print("\033[0;32m [Success]The file is stored in {path}\033[0m".format(
                path=replace_last(self.path, ".enc", ".dec")))

    # compress the file using LZ78 coding
    def LZ78_compress(self, output_path: str = None) -> None:
        # check if the file is already compressed with my file format
        File_Head = b"ZCLZ"
        if output_path:
            f = open(output_path, "wb")
        else:
            f = open(self.path + ".enc", "wb")
        f.write(File_Head)
        # encode the file
        self.dic = LZ78.Encode(self.filecontent, self.dic)
        index = 0
        length = len(self.dic)
        while index < length:
            if index == 0:
                data = self.dic[index][0] + \
                    self.dic[index][1].to_bytes(1, byteorder='big')
            else:
                data = self.dic[index][0] + self.dic[index][1].to_bytes(
                    int(log(index, 256))+1, byteorder='big')
            f.write(data)
            index += 1
        f.close()
        print("\033[0;32m [Success]Compress successfully!\033[0m")
        print("\033[0;32m [Success]The file is stored in {path}\033[0m".format(
            path=output_path if output_path else self.path + ".enc"))

    # decompress the file using LZ78 coding
    def LZ78_decompress(self, output_path: str = None) -> None:
        # check if the file is already compressed with my file format
        File_Head = b"ZCLZ"
        encoded_data = self.filecontent
        # check if the file is already compressed with my file format
        if encoded_data[:4] != File_Head:
            print(
                "\033[0;31m [Error]The file is not compressed with my algorithm\033[0m")
            exit(0)
        encoded_data = encoded_data[4:]
        # Recover the dictionary
        index = 0
        length = len(encoded_data)
        while index < length:
            if index == 0:
                data = [bytes([encoded_data[index]]), encoded_data[index+1]]
                index += 2
                self.dic.append(data)
                continue
            else:
                if index+int(log(index, 256))+2 > length:
                    data = [b'', int.from_bytes(
                        encoded_data[index:], byteorder='big')]
                    self.dic.append(data)
                    break
                data = [bytes([encoded_data[index]]), int.from_bytes(
                    encoded_data[index+1:index+int(log(len(self.dic), 256))+2], byteorder='big')]
                index += int(log(len(self.dic), 256))+2
                self.dic.append(data)
                continue
        # Decode the file
        decoded_data = LZ78.Decode(self.dic)
        if output_path:
            f = open(output_path, "wb")
        else:
            f = open(replace_last(self.path, ".enc", ".dec"), "wb")
        f.write(b"".join(decoded_data))
        print("\033[0;32m [Success]Decompress successfully!\033[0m")
        print("\033[0;32m [Success]The file is stored in {path}\033[0m".format(
            path=output_path if output_path else replace_last(self.path, ".enc", ".dec")))


if __name__ == "__main__":
    # filepath = "HuffmanTest/ico.zip"
    # zcoder = Zcoder(filepath)
    # zcoder.Huffman_compress()
    # zcode = Zcoder(filepath + ".enc")
    # zcode.Huffman_decompress()
    filepath = "LZTest/ELF"
    zcoder = Zcoder(filepath)
    zcoder.LZ78_compress()
    zcoder = Zcoder(filepath + ".enc")
    zcoder.LZ78_decompress()
