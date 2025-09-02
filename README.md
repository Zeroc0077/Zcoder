# Zcoder

a tool for some easy encode(Huffman and LZ78)

## Usage

```bash           
git clone https://github.com/Zeroc0077/Zcoder.git

cd Zcoder

python main.py -h

 Welcome to Zcoder!!! 


  ______             _           
 |___  /            | |          
    / / ___ ___   __| | ___ _ __ 
   / / / __/ _ \ / _` |/ _ \ '__|
  / /_| (_| (_) | (_| |  __/ |   
 /_____\___\___/ \__,_|\___|_|


usage: python main.py [OPTION...] [-i INPUT] [-o OUTPUT]

file compressor and decompressor

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        the absolute or relative path of the input file
  -o [OUTPUT], --output [OUTPUT]
                        the absolute or relative path of the output file
  -c, --compress        input files to compress
  -d, --decompress      input files to decompress
  -H, --Huffman         use Huffman coding to compress the file
  -L, --LZ              use LZ coding to compress the file
  -T file1 file2        test the file before compression and after decompression
```

the `channel/lab2_program_linux_amd64.run` is a test program that can be used to test the your hamming encode/decode program. The `phase` stands for different error rate. The `mode` stands for the different mode of the program. Like `source`, `channel`, `verify`.

`Usage`:
```bash
./lab2_program_linux_amd64.run -mode=source -phase=1 | python hamming_encode.py | ./lab2_program_linux_amd64.run -mode=channel -phase=1 | python hamming_decode.py | ./lab2_program_linux_amd64.run -mode=verify -phase=1
```

## Test

some test file can stored in the encode_test folder.
