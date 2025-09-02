import numpy as np
import random

# The test matrix
H = np.mat([
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
])
# The generator matrix
G = np.mat([
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1]
])


def channel_error(bits: str) -> str:
    """
    stimulate the channel error
    """
    index = random.randint(0, len(bits) - 1)
    # print(f"[channel error]the error bit is {index+1}")
    bits = list(bits)
    bits[index] = str(int(bits[index]) ^ 1)
    return ''.join(bits)


def hamming_encode(bits: str) -> str:
    """
    Implement the hamming encode algorithm using Matrix Multiplication
    """
    b = np.mat([int(i) for i in bits])
    code = b * G % 2
    return ''.join([str(i) for i in code.tolist()[0]])


def hamming_decode(bits: str, error: bool = False) -> str:
    """
    Implement the hamming decode algorithm using Matrix Multiplication
    """
    if error:
        bits = channel_error(bits)
    b = np.mat([int(i) for i in bits])
    error = b * H.T % 2
    error = int(''.join(str(i) for i in error.tolist()[0][::-1]), 2)
    bits = list(bits)
    if error:
        # print(f"[hamming decode]the error bit is {error}")
        bits[error - 1] = str(int(bits[error - 1]) ^ 1)
    code = []
    p = 0
    for i in range(len(bits)):
        if np.power(2, p) - 1 != i:
            code.append(int(bits[i]))
        else:
            p += 1
    return ''.join([str(i) for i in code])


def optimize_hamming_encode(bits: str) -> str:
    """
    Implement the hamming encode algorithm using even/odd parity
    """
    bits = list(bits)
    # calculate the number of parity bits
    parity_bits = 0
    while 2 ** parity_bits < len(bits) + parity_bits + 1:
        parity_bits += 1

    # insert parity bits
    encoded_bits = [None] * (len(bits) + parity_bits)
    j = 0
    for i in range(len(encoded_bits)):
        if i + 1 == 2**j:
            encoded_bits[i] = 0
            j += 1
        else:
            encoded_bits[i] = int(bits.pop(0))
    # calculate the value of parity bits
    for i in range(parity_bits):
        position = 2**i
        count = 0
        for j in range(position, len(encoded_bits)):
            if ((j+1) >> i) & 1 == 1 and encoded_bits[j] == 1:
                count ^= 1
        encoded_bits[position-1] = count % 2
    return "".join(str(i) for i in encoded_bits)


def optimize_hamming_decode(bits: str, error: bool = False) -> str:
    """
    Implement the hamming decode algorithm using even/odd parity
    """
    if error:
        bits = channel_error(bits)
    bits = list(bits)
    # test error
    error_position = 0
    for i in range(len(bits)):
        if bits[i] == '1':
            error_position ^= (i+1)
    # adjust error
    if error_position > 0:
        bits[error_position-1] = str(int(bits[error_position-1]) ^ 1)

    # extract data bits
    decoded_bits = ''
    j = 0
    for i in range(len(bits)):
        if i + 1 != 2**j:
            decoded_bits += bits[i]
        else:
            j += 1

    return decoded_bits


def _extend(bits: str) -> str:
    """
    add the extend test bit
    """
    ex = 0
    for i in range(len(bits)):
        if bits[i] == "1":
            ex += 1
    return bits + str(ex % 2)


def two_bits_error_ocurr(bits: str) -> str:
    """
    stimulate the two bits error ocurr
    """
    index1 = random.randint(0, len(bits) - 1)
    # print(f"[channel error]the error bit is {index1+1}")
    bits = list(bits)
    bits[index1] = str(int(bits[index1]) ^ 1)
    index2 = random.randint(0, len(bits) - 1)
    while index2 == index1:
        index2 = random.randint(0, len(bits) - 1)
    # print(f"[channel error]the error bit is {index2+1}")
    bits[index2] = str(int(bits[index2]) ^ 1)
    return ''.join(bits)


def decode_with_two_bits_error_detect(bits: str, error: bool = True) -> str:
    """
    hammind decode with two bits error detect
    """
    if error:
        bits = two_bits_error_ocurr(bits)
    error_position = 0
    for i in range(len(bits)-1):
        if bits[i] == '1':
            error_position ^= (i+1)
    if error_position == 0:
        return bits[2] + bits[4:7] + bits[8:15]
    error_position -= 1
    bits = bits[:error_position] + \
        str(int(bits[error_position]) ^ 1) + bits[error_position+1:]
    tmp = optimize_hamming_encode(bits[2] + bits[4:7] + bits[8:15])
    tmp = _extend(tmp)
    if tmp[-1] == bits[-1]:
        return bits[2] + bits[4:7] + bits[8:15]
    else:
        return "False"


if __name__ == "__main__":
    date = open("./hamming_15_11.txt", "r")
    lines = date.readlines()
    for i in lines:
        line = i.strip()
        origin, code = line.split(", ")
        # test hamming encode
        test_code = optimize_hamming_encode(origin)
        assert test_code == code, f"encode error: {origin} -> {test_code} != {code}"
        # test hamming decode
        test_origin = optimize_hamming_decode(code)
        assert test_origin == origin, f"decode error: {code} -> {test_origin} != {origin}"
        # test hamming decode with error
        test_error_code = optimize_hamming_decode(code, error=True)
        assert test_error_code == origin, f"decode error: {code} -> {test_error_code} != {origin}"
        test_two_error_code = _extend(optimize_hamming_encode(origin))
        detect = decode_with_two_bits_error_detect(test_two_error_code)
        assert detect == "False", f"two error detect error: {test_two_error_code} -> {detect} != False"
    print("All test passed!")
