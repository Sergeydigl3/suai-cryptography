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

        for i in range(0, len(data) - 2 * self.block_size, self.block_size):
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

        # encrypted_data.extend(padding_size.to_bytes(self.block_size, byteorder='big'))

        return encrypted_data

    def encrypt_cbc(self, data, iv):
        encrypted_data = bytearray()
        padding_size = len(data) % self.block_size
        encrypted_data.extend(padding_size.to_bytes(4, byteorder='big'))
        print(padding_size)
        for i in range(0, len(data), self.block_size):
            block = data[i:i + self.block_size]
            if len(block) < self.block_size:
                padding_size = self.block_size - len(block)
                block = block + b'\x00' * padding_size
            block = bytes([a ^ b for a, b in zip(block, iv)])
            encrypted_block = self.encrypt_block(block)
            encrypted_data.extend(encrypted_block)
            iv = encrypted_block
        print(padding_size)
        # last block is Int padded bytes

        return encrypted_data

    def decrypt_cbc(self, data, iv, padding_size=0):
        decrypted_data = bytearray()
        for i in range(0, len(data) - self.block_size, self.block_size):
            block = data[i:i + self.block_size]
            decrypted_block = self.decrypt_block(block)
            decrypted_block = bytes([a ^ b for a, b in zip(decrypted_block, iv)])
            decrypted_data.extend(decrypted_block)
            iv = block

        # padding_size = int.from_bytes(data[-self.block_size:], byteorder='big')
        last_block = data[-self.block_size:]
        decrypted_block = self.decrypt_block(last_block)
        decrypted_block = bytes([a ^ b for a, b in zip(decrypted_block, iv)])
        if padding_size != 0:
            decrypted_data.extend(decrypted_block[:-padding_size])
        else:
            decrypted_data.extend(decrypted_block)
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


import struct
from PIL import Image, ImageDraw, ImageFont


def add_text_to_image(input_image_path, output_image_path, text_to_add):
    # copy file to new file
    # with open(input_image_path, 'rb') as f:
    #     with open(output_image_path, 'wb') as f2:
    #         f2.write(f.read())
    try:
        original_image = open(input_image_path, 'rb')
        original_header = original_image.read(10)
        offset_bytes = original_image.read(4)
        original_header += offset_bytes
        offset = struct.unpack('I', offset_bytes)[0]
        original_image.read(20)
        image_array_size = struct.unpack('I', original_image.read(4))[0]
        print(image_array_size)
        print("ALERT")
        # width_bytes = struct.unpack('I', original_image.read(4))[0]
        # height_bytes = struct.unpack('I', original_image.read(4))[0]

        # original_header += original_image.read(offset - 14)

        original_image.close()


        # Открытие изображения
        image = Image.open(input_image_path)


        # Создание объекта для рисования
        draw = ImageDraw.Draw(image)

        # Загрузка шрифта
        font = ImageFont.load_default()

        # Масштабирование шрифта до нужного размера

        # Определение позиции текста
        text_position = (20, 20)  # Позиция, в которой будет нарисован текст

        # Нанесение текста на изображение
        draw.text(text_position, text_to_add, fill="black", font=font)

        # Сохранение измененного изображения
        image.save(output_image_path)
        # new_file = open(output_image_path, 'wb')
        # i
        print(f"Текст успешно добавлен в {output_image_path}")

    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

# def add_text_to_image(input_image_path, output_image_path, text_to_add):
#     try:
#         image = Image.open(input_image_path)
#         draw = ImageDraw.Draw(image)
#
#         font = ImageFont.load_default()
#
#         width, height = image.size
#         cell_width = 20
#         cell_height = 20
#
#         for y in range(0, height, cell_height):
#             for x in range(0, width, cell_width):
#                 text_width, text_height = draw.textsize(text_to_add, font=font)
#                 text_position = (x, y)
#                 if text_position[0] + text_width <= width and text_position[1] + text_height <= height:
#                     draw.text(text_position, text_to_add, fill="black", font=font)
#
#         # Сохранение измененного изображения
#         image.save(output_image_path)
#         print(f"Текст успешно добавлен в {output_image_path}")
#
#     except Exception as e:
#         print(f"Произошла ошибка: {str(e)}")


class CryptoWrapper:
    def __init__(self, cipher):
        self.cipher = cipher

    def encrypt(self, data):
        return self.cipher.encrypt(data)

    def decrypt(self, data):
        return self.cipher.decrypt(data)

    def encrypt_file(self, filename, output_filename, bmp=False, mode='ECB'):

        with open(filename, 'rb') as f:

            if bmp:
                bmp_header = f.read(10)
                offset = struct.unpack('I', f.read(4))[0]
                bmp_header += (offset + 4).to_bytes(4, byteorder='little')
                bmp_header += f.read(offset - 14)
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

    def decrypt_file(self, filename, output_filename, bmp=False, mode='ECB'):

        with open(filename, 'rb') as f:

            if bmp:
                bmp_header = f.read(10)
                offset = struct.unpack('I', f.read(4))[0]
                bmp_header += (offset - 4).to_bytes(4, byteorder='little')
                bmp_header += f.read(offset - 18)
            padding_size = int.from_bytes(f.read(4), byteorder='little')


            data = f.read()

        if mode == 'ECB':
            decrypted_data = self.decrypt(data)
        elif mode == 'CBC':
            decrypted_data = self.cipher.decrypt_cbc(data, b'\x00' * self.cipher.block_size, padding_size=padding_size)
        else:
            raise ValueError('Unknown mode')

        with open(output_filename, 'wb') as f:

            if bmp:
                f.write(bmp_header)

            f.write(decrypted_data)
