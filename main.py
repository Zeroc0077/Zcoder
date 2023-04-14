# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2023/03/27 10:44:49
@Author  :   zeroc 
'''
import sys
sys.dont_write_bytecode = True
import argparse
import os
from Zcoder import Zcoder

# compare two files' sha256
def test(path1, path2):
    hash1 = os.popen("sha256sum " + path1).read().split(" ")[0]
    hash2 = os.popen("sha256sum " + path2).read().split(" ")[0]
    print(f"\033[0;34m The sha256 of file1 is {hash1}\033[0m")
    print(f"\033[0;34m The sha256 of file2 is {hash2}\033[0m")
    if hash1 == hash2:
        print("\033[0;34m The two files are the same!\033[0m")
    else:
        print("\033[0;31m The two files are different!\033[0m")


banner = """
\033[0;35m
  ______             _           
 |___  /            | |          
    / / ___ ___   __| | ___ _ __ 
   / / / __/ _ \ / _` |/ _ \ '__|
  / /_| (_| (_) | (_| |  __/ |   
 /_____\___\___/ \__,_|\___|_|
\033[0m
"""
print("\033[0;33m Welcome to Zcoder!!! \033[0m")
print(banner)

parser = argparse.ArgumentParser(
    prog='main.py',
    description='file compressor and decompressor',
    usage='python main.py [OPTION...] [-i INPUT] [-o OUTPUT]'
)
parser.add_argument('-i', '--input', type=str,
                    help='the absolute or relative path of the input file')
parser.add_argument('-o', '--output', type=str, nargs="?", default=None,
                    help='the absolute or relative path of the output file')
group1 = parser.add_mutually_exclusive_group()
group2 = parser.add_mutually_exclusive_group()
group1.add_argument('-c', '--compress', action="store_true",
                    help='input files to compress')
group1.add_argument('-d', '--decompress', action="store_true",
                    help='input files to decompress')
group2.add_argument('-H', '--Huffman', action='store_true',
                    help='use Huffman coding to compress the file')
group2.add_argument('-L', '--LZ', action='store_true',
                    help='use LZ coding to compress the file')
group2.add_argument('-T', nargs=2, metavar=("file1", "file2"),
                    help='test the file before compression and after decompression')
try:
    args = parser.parse_args()
except Exception as e:
    print(f"\033[0;31m {e}\033[0m")
    exit(0)

if not args.Huffman and not args.LZ and not args.T:
    print("\033[0;31m [Error]You must choose one method!\033[0m")
    exit(0)
if not args.compress and not args.decompress and not args.T:
    print("\033[0;31m [Error]You must choose one option!\033[0m")
    exit(0)

if args.compress:
    try:
        if not os.path.exists(args.input):
            print("\033[0;31m [Error]The input file does not exist!\033[0m")
            exit(0)
    except Exception as e:
        print(f"\033[0;31m {e}\033[0m")
        exit(0)
    if args.Huffman:
        Zcoder(args.input).Huffman_compress(args.output)
        exit(0)
    if args.LZ:
        Zcoder(args.input).LZ78_compress(args.output)
        exit(0)
if args.decompress:
    try:
        if not os.path.exists(args.input):
            print("\033[0;31m [Error]The input file does not exist!\033[0m")
            exit(0)
    except Exception as e:
        print(f"\033[0;31m {e}\033[0m")
        exit(0)
    if args.Huffman:
        Zcoder(args.input).Huffman_decompress(args.output)
        exit(0)
    if args.LZ:
        Zcoder(args.input).LZ78_decompress(args.output)
        exit(0)
if args.T:
    try:
        test(args.T[0], args.T[1])
        exit(0)
    except Exception as e:
        print(f"\033[0;31m {e}\033[0m")
        exit(0)
