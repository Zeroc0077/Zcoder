# -*- encoding: utf-8 -*-
'''
@File    :   Huffman.py
@Time    :   2023/03/28 12:19:22
@Author  :   zeroc 
'''
from tqdm import tqdm
from math import ceil


class TreeNode:
    def __init__(self, char, freq: int = None, code: str = None):
        self.isroot = False  # judge if it's the root
        self.char = char  # character
        self.freq = freq  # frequency of the character
        self.left = None  # left child
        self.right = None  # right child
        self.code = code  # code of the character


# Defining a class for Huffman coding
class HuffmanCoding:
    @staticmethod
    def _MakeFrequencyDict(content: bytes) -> dict[bytes, int]:
        """
        make a frequency dictionary according to the content
        Arguments:
        - content: bytes, the content of the file
        Returns:
        - dic: dict, the frequency dictionary
        """
        dic = [0 for _ in range(256)]
        for char in content:
            dic[char] += 1
        return {bytes([i]): j for i, j in enumerate(dic) if j != 0}

    @staticmethod
    def _ConstructCodeBook(dic: dict[bytes, int]) -> dict[bytes, str]:
        """
        make a codebook according to the frequency dictionary
        Arguments:
        - dic: dict[bytes, int], the frequency dictionary
        Returns:
        - codebook: dict[bytes, str], the codebook
        """
        codebook = {}

        def _ConstructCodeBookRec(node: TreeNode, code: str) -> None:
            """
            assign a value to node recursively
            Arguments:
            - node: TreeNode, the node to be assigned
            - code: str, the codeword of the node
            """
            if node is None:
                return
            if node.char is not None:
                node.code = code
                codebook[node.char] = code
            _ConstructCodeBookRec(node.left, code + '0')
            _ConstructCodeBookRec(node.right, code + '1')

        # the file only contains one character
        if len(dic) == 1:
            return {list(dic.keys())[0]: '0'}
        # initialize the Huffman tree
        nodelist = [TreeNode(char=i, freq=j) for i, j in dic.items()]
        nodelist = sorted(nodelist, key=lambda x: x.freq, reverse=True)
        # construct the Huffman tree
        while len(nodelist) != 1:
            left = nodelist.pop(-1)
            right = nodelist.pop(-1)
            newnode = TreeNode(char=None, freq=left.freq + right.freq)
            newnode.left = left
            newnode.right = right
            nodelist.append(newnode)
            nodelist = sorted(nodelist, key=lambda x: x.freq, reverse=True)
        _ConstructCodeBookRec(nodelist[0], '')
        return codebook

    @classmethod
    def Canonical(cls, codebook: dict[bytes, str]) -> dict[bytes, str]:
        """
        transform the huffman dictionary to the canonical form
        Arguments:
        - codebook: dict[bytes, str], the codebook
        Returns:
        - canonical codebook: dict[bytes, str], the canonical codebook
        """
        codelist = [(i, len(j)) for i, j in codebook.items()]
        # sort the codebook according to the length and then the value
        codelist = sorted(codelist, key=lambda x: (x[1], x[0]))
        value, length = [], []
        for i, j in codelist:
            value.append(i)
            length.append(j)
        return cls._ReConstruct(value, length)

    @staticmethod
    def _ReConstruct(value: list[bytes], length: list[int]) -> dict[bytes, str]:
        """
        reconstruct the codebook to the canonical form
        Arguments:
        - value: list[bytes], the value of the codebook
        - length: list[int], the length of the codebook's codeword
        Returns:
        - codebook: dict[bytes, str], the canonical codebook
        """
        canon_dic = {}
        code = 0
        for i in range(len(value)):
            if i == 0:
                code = 0
            else:
                code = (code + 1) << (length[i] - length[i - 1])
            canon_dic[value[i]] = bin(code)[2::].rjust(length[i], '0')
        return canon_dic

    @staticmethod
    def _RecoverHuffmanTree(codebook: dict[bytes, str]) -> TreeNode:
        """
        recover the Huffman tree according to the codebook
        Arguments:
        - codebook: dict[bytes, str], the codebook
        Returns:
        - root: TreeNode, the root of the Huffman tree
        """
        nodelist = [TreeNode(char=i, code=j) for i, j in codebook.items()]
        while len(nodelist) != 1:
            nodelist = sorted(nodelist, key=lambda x: (len(x.code), x.code))
            right = nodelist.pop(-1)
            left = nodelist.pop(-1)
            newnode = TreeNode(char=None, code=left.code[:-1])
            newnode.left = left
            newnode.right = right
            nodelist.append(newnode)
        return nodelist[0]

    @staticmethod
    def Encode(content: bytes, codebook: dict[bytes, str]) -> tuple[bytes, int]:
        """
        encode the content according to the codebook
        Arguments:
        - content: bytes, the content of the file
        - codebook: dict[bytes, str], the codebook
        Returns:
        - encoded content: bytes, the encoded content
        - padding: int, the number of padding bits
        """
        encoded_content = ''
        dic = [bytes([item]) for item in range(256)]
        a = [dic[item] for item in content]
        for item in tqdm(a, desc='Encoding'):
            encoded_content += codebook[item]
        padding = ceil(len(encoded_content) / 8) * 8 - len(encoded_content)
        encoded_content += '0' * padding
        encoded_content = int(encoded_content, 2).to_bytes(
            len(encoded_content) // 8, 'big')
        return encoded_content, padding

    @staticmethod
    def Decode(encoded_content: bytes, padding: int, codebook: dict[bytes, str]) -> bytes:
        """
        decode the encoded content according to the codebook
        Arguments:
        - encoded content: bytes, the encoded content
        - padding: int, the number of padding bits
        - codebook: dict[bytes, str], the codebook
        Returns:
        - decoded content: bytes, the decoded content
        """
        if len(codebook) == 1:
            codebook[256] = "1"
        # get the root node of the huffman tree
        rootnode = HuffmanCoding._RecoverHuffmanTree(codebook)
        decode_content = []
        # transform the encoded content to binary sequence
        binary_str = list("".join(bin(i)[2:].rjust(8, "0") for i in encoded_content)[
            :-padding] if padding > 0 else "".join(bin(i)[2:].rjust(8, "0") for i in encoded_content))

        node = rootnode
        for i in tqdm(range(0, len(binary_str), 8), desc='Decoding'):
            for j in binary_str[i:i+8]:
                if j == '0':
                    node = node.left
                else:
                    node = node.right
                if node.left is None and node.right is None:
                    decode_content.append(node.char)
                    node = rootnode
        return bytes(decode_content)
