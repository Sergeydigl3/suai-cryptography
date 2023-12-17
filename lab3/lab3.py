def series_test(data):
    print("Последовательностей разрывов")
    bits = int.from_bytes(data, byteorder='big')
    entry_nul = ""
    nul = ""
    one = ""

    for k in range(63, -1, -1):
        nul += "0"
        one += "1"
        entry_nul += "1" if bits & (1 << k) else "0"

    entry_one = entry_nul
    X = 0

    for i in range(63, -1, -1):
        count = entry_nul.count(nul)
        entry_nul = entry_nul.replace(nul, "")
        nul = nul[:-1]

        if count != 0:
            print(f"длиной {i + 1} = {count}")
            e = (64 - i + 4) / (2 ** (i + 3))
            X += (count - e) ** 2 / e

    print("Последовательностей блоков")
    for i in range(63, -1, -1):
        count = entry_one.count(one)
        entry_one = entry_one.replace(one, "")
        one = one[:-1]

        if count != 0:
            print(f"длиной {i + 1} = {count}")
            e = (64 - i + 4) / (2 ** (i + 4))
            X += (count - e) ** 2 / e

    print(f"Статистика Х = {X}")


# Example usage:
input_bytes = b'\x01\x23\x45\x67\x89\xab\xcd\xef'
series_test(input_bytes)

if __name__ == '__main__':

