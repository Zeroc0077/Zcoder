def optimize_hamming_decode(bits: str) -> str:
    """
    Implement the hamming decode algorithm using even/odd parity
    """
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


if __name__ == "__main__":
    import sys
    code = sys.stdin.read(15)
    while len(code) != 0:
        sys.stdout.write(optimize_hamming_decode(code))
        code = sys.stdin.read(15)
