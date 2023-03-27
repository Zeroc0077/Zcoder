# -*- encoding: utf-8 -*-
'''
@File    :   main.py
@Time    :   2023/03/27 10:44:49
@Author  :   zeroc 
'''
import argparse

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

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))