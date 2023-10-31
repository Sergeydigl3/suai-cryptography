import random
from icecream import ic


class JeffersonCylinder2BlockCipher:
    def __init__(self, disks, block_size=16, difference=4, round_count=16):
        self.disks = disks.copy()
        self.difference = difference
        self.round_count = round_count
        self.block_size = block_size

    def decrypt_block(self, block_origin):
        block = bytearray(block_origin)
        for i in range(self.round_count):
            for j, byte_element in enumerate(block):
                disk = self.disks[j % len(self.disks)]
                index = (disk.find(byte_element) - self.difference) % len(disk)
                block[j] = disk[index]

        return block

    def decrypt(self, data):

        decrypted_data = bytearray()

        for i in range(0, len(data) - self.block_size, self.block_size):
            block = data[i:i + self.block_size]
            decrypted_block = self.decrypt_block(block)
            decrypted_data.extend(decrypted_block)

        padding_size = int.from_bytes(data[-self.block_size:], byteorder='big')
        last_block = data[-self.block_size * 2:-self.block_size]
        decrypted_block = self.decrypt_block(last_block)
        if padding_size != 0:
            decrypted_data.extend(decrypted_block[:-padding_size])
        return decrypted_data

    def encrypt_block(self, block_origin):
        block = bytearray(block_origin)

        for i in range(self.round_count):

            for j, byte_element in enumerate(block):
                disk = self.disks[j % len(self.disks)]
                index = (disk.find(byte_element) + self.difference) % len(disk)
                block[j] = disk[index]

        return block

    def encrypt(self, data):
        encrypted_data = bytearray()
        padding_size = 0
        for i in range(0, len(data), self.block_size):
            block = data[i:i + self.block_size]
            if len(block) < self.block_size:
                padding_size = self.block_size - len(block)
                block = block + b'\x00' * padding_size
            encrypted_block = self.encrypt_block(block)
            encrypted_data.extend(encrypted_block)

        # last block is Int padded bytes

        encrypted_data.extend(padding_size.to_bytes(self.block_size, byteorder='big'))

        return encrypted_data

    def encrypt_cbc(self, data, iv):
        encrypted_data = bytearray()
        padding_size = 0
        for i in range(0, len(data), self.block_size):
            block = data[i:i + self.block_size]
            if len(block) < self.block_size:
                padding_size = self.block_size - len(block)
                block = block + b'\x00' * padding_size
            block = bytes([a ^ b for a, b in zip(block, iv)])
            encrypted_block = self.encrypt_block(block)
            encrypted_data.extend(encrypted_block)
            iv = encrypted_block

        # last block is Int padded bytes

        encrypted_data.extend(padding_size.to_bytes(self.block_size, byteorder='big'))

        return encrypted_data

    def decrypt_cbc(self, data, iv):
        decrypted_data = bytearray()
        for i in range(0, len(data) - self.block_size, self.block_size):
            block = data[i:i + self.block_size]
            decrypted_block = self.decrypt_block(block)
            decrypted_block = bytes([a ^ b for a, b in zip(decrypted_block, iv)])
            decrypted_data.extend(decrypted_block)
            iv = block

        padding_size = int.from_bytes(data[-self.block_size:], byteorder='big')
        last_block = data[-self.block_size * 2:-self.block_size]
        decrypted_block = self.decrypt_block(last_block)
        decrypted_block = bytes([a ^ b for a, b in zip(decrypted_block, iv)])
        if padding_size != 0:
            decrypted_data.extend(decrypted_block[:-padding_size])
        return decrypted_data

    @staticmethod
    def generate_disks(disk_count=16) -> list[bytes]:

        all_bytes = bytearray()  # 256 bytes
        for i in range(256):
            all_bytes.append(i)

        mixed_universal_disks = [
            bytes(random.sample(all_bytes, len(all_bytes))) for _ in range(disk_count)
        ]

        return mixed_universal_disks

    @staticmethod
    def save_disks(disks, filename='disks.txt'):
        with open(filename, 'wb') as f:
            # first byte is disk count
            # every disk is 256 bytes
            f.write(len(disks).to_bytes(1, byteorder='big'))
            for disk in disks:
                f.write(disk)

    @staticmethod
    def load_disks(filename='disks.txt'):
        disks: list[bytes] = []
        with open(filename, 'rb') as f:
            disk_count = int.from_bytes(f.read(1), byteorder='big')
            ic(disk_count)
            for _ in range(disk_count):
                disks.append(f.read(256))

        return disks


class CryptoWrapper:
    def __init__(self, cipher):
        self.cipher = cipher

    def encrypt(self, data):
        return self.cipher.encrypt(data)

    def decrypt(self, data):
        return self.cipher.decrypt(data)

    def encrypt_file(self, filename, output_filename=None, bmp=False, mode='ECB'):
        if output_filename is None:
            if bmp:
                output_filename = filename + '.enc.bmp'
            else:
                output_filename = filename + '.enc'

        with open(filename, 'rb') as f:
            if bmp:
                bmp_header = f.read(54)
            data = f.read()

        # encrypted_data = self.encrypt(data)
        if mode == 'ECB':
            encrypted_data = self.encrypt(data)
        elif mode == 'CBC':
            encrypted_data = self.cipher.encrypt_cbc(data, b'\x00' * self.cipher.block_size)
        else:
            raise ValueError('Unknown mode')

        with open(output_filename, 'wb') as f:
            if bmp:
                f.write(bmp_header)
            f.write(encrypted_data)

    def decrypt_file(self, filename, output_filename=None, bmp=False, mode='ECB'):
        if output_filename is None:
            output_filename = filename + '.dec'

        with open(filename, 'rb') as f:

            if bmp:
                bmp_header = f.read(54)

            data = f.read()

        if mode == 'ECB':
            decrypted_data = self.decrypt(data)
        elif mode == 'CBC':
            decrypted_data = self.cipher.decrypt_cbc(data, b'\x00' * self.cipher.block_size)
        else:
            raise ValueError('Unknown mode')

        with open(output_filename, 'wb') as f:

            if bmp:
                f.write(bmp_header)

            f.write(decrypted_data)
