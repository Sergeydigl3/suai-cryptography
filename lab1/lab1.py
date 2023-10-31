import random


class JeffersonCylinder:
    def __init__(self, disks):
        self.disks = disks

    def encrypt(self, message):
        encrypted_message = []
        for i, char in enumerate(message):
            if char.isalpha():
                disk = self.disks[i % len(self.disks)]
                if char in ru_alphabet:
                    alphabet_language_start = ord('А')
                else:
                    alphabet_language_start = ord('A')
                index = ord(char.upper()) - alphabet_language_start
                encrypted_message.append(disk[index])
            else:
                encrypted_message.append(char)

        return ''.join(encrypted_message)

    def decrypt(self, message):
        decrypted_message = []
        for i, char in enumerate(message):
            if char.isalpha():
                disk = self.disks[i % len(self.disks)]
                index = disk.find(char.upper())
                if char in ru_alphabet:
                    alphabet_language_start = ord('А')
                else:
                    alphabet_language_start = ord('A')
                decrypted_message.append(chr(alphabet_language_start + index))
            else:
                decrypted_message.append(char)

        return ''.join(decrypted_message)


class JeffersonCylinder2:
    def __init__(self, disks, difference=4):
        self.disks = disks
        self.difference = difference

    def encrypt(self, message):
        encrypted_message = []
        for i, char in enumerate(message):
            if char.isalpha():
                disk = self.disks[i % len(self.disks)]
                # find char in the disk and add difference and pick that char from disk by index
                index = (disk.find(char.upper()) + self.difference) % len(disk)
                encrypted_message.append(disk[index])
            else:
                encrypted_message.append(char)

        return ''.join(encrypted_message)

    def decrypt(self, message):
        decrypted_message = []
        for i, char in enumerate(message):
            if char.isalpha():
                disk = self.disks[i % len(self.disks)]
                # find char in the disk and subtract difference and pick that char from disk by index
                index = (disk.find(char.upper()) - self.difference) % len(disk)
                decrypted_message.append(disk[index])
            else:
                decrypted_message.append(char)

        return ''.join(decrypted_message)


def frequency_analysis(text):
    frequency = {}
    for char in text:
        if char.isalpha():
            char = char.upper()
            if char not in frequency:
                frequency[char] = 1
            else:
                frequency[char] += 1

    return frequency


ru_alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЪЭЮЯ"
en_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

mixed_ru_alphabet = random.sample(ru_alphabet, len(ru_alphabet))
# Example usage:
disks = [
    "DMTWSILRUYQNKFEJCAZBPGXOHV",
    "EJOTYCHMRWAFKPUZDINSXBGLQV",
    "BHIPLTXNZRFYGKQJSOCEVUAMWD",
]

ru_disks_random = [
    # as str
    ''.join(random.sample(ru_alphabet, len(ru_alphabet))),
    ''.join(random.sample(ru_alphabet, len(ru_alphabet))),
    ''.join(random.sample(ru_alphabet, len(ru_alphabet))),
]

mixed_universal_alphabet = random.sample(en_alphabet + ru_alphabet, len(en_alphabet + ru_alphabet))

mixed_universal_disks = [
    ''.join(random.sample(mixed_universal_alphabet, len(mixed_universal_alphabet))),
    ''.join(random.sample(mixed_universal_alphabet, len(mixed_universal_alphabet))),
    ''.join(random.sample(mixed_universal_alphabet, len(mixed_universal_alphabet))),
]

ru_disks_metoda = [
    "ЪИЖГОПА",
    "ОЕУКПВР",
    "СРТОЕКУ",
    "МАФДРКЦ",
    "АРГШЩЗХ",
    "РХПАСЧЯ"
]

if __name__ == '__main__':
    cylinder = JeffersonCylinder2(disks)
    cylinder_metoda = JeffersonCylinder2(ru_disks_metoda)
    cylinder_ru = JeffersonCylinder2(ru_disks_random)

    message = "HELLO WORLD"
    message_ru = "ПРИВЕТ МИР"
    message_metoda = "иерарх"

    encrypted_message = cylinder.encrypt(message)
    decrypted_message = cylinder.decrypt(encrypted_message)
    print("ENGLISH ALPHABET")
    print(f"Original message: {message}")
    print(f"Encrypted message: {encrypted_message}")
    print(f"Decrypted message: {decrypted_message}\n\n")

    # message_ru

    encrypted_message = cylinder_ru.encrypt(message_ru)
    decrypted_message = cylinder_ru.decrypt(encrypted_message)
    print("RUSSIAN ALPHABET")
    print(f"Original message: {message_ru}")
    print(f"Encrypted message: {encrypted_message}")
    print(f"Decrypted message: {decrypted_message}\n\n")

    # message_metoda

    encrypted_message = cylinder_metoda.encrypt(message_metoda)
    decrypted_message = cylinder_metoda.decrypt(encrypted_message)
    print("METODA ALPHABET")
    print(f"Original message: {message_metoda}")
    print(f"Encrypted message: {encrypted_message}")
    print(f"Decrypted message: {decrypted_message}\n\n")

    # freq_analysis_result = frequency_analysis(encrypted_message)
    # print(f"Frequency analysis: {freq_analysis_result}")

    print("MIXED ALPHABET")
    cylinder_mixed = JeffersonCylinder(mixed_universal_disks)
    message_mixed = "HELLO МИР1ВСЕМ"
    encrypted_message = cylinder_mixed.encrypt(message_mixed)
    decrypted_message = cylinder_mixed.decrypt(encrypted_message)
    print(f"Original message: {message_mixed}")
    print(f"Encrypted message: {encrypted_message}")
    print(f"Decrypted message: {decrypted_message}\n\n")

