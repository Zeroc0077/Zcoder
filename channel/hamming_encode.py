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


if __name__ == "__main__":
    import sys
    text = sys.stdin.read(11)
    while len(text) != 0:
        sys.stdout.write(optimize_hamming_encode(text))
        text = sys.stdin.read(11)
