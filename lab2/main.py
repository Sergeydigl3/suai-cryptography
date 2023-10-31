from lab2new import JeffersonCylinder2BlockCipher as JC
from lab2new import CryptoWrapper as CW

if __name__ == '__main__':
    block_size = 4
    round_count = 2
    disks = JC.generate_disks(block_size)
    # JC.save_disks(disks)
    # disks = JC.load_disks()
    jf = JC(disks, block_size, round_count=round_count)
    # jf.encrypt_file('hello.txt')
    #
    # jf.decrypt_file('hello.txt.enc')
    cw = CW(jf)
    # cw.encrypt_file('test_data/mars/mars2.png')
    #
    # cw.decrypt_file('test_data/mars/mars2.png.enc', 'test_data/mars/mars2.dec.png')



    # cw.encrypt_file('test_data/suai/suai.bmp', 'test_data/suai/suia.enc.bmp', bmp=True, mode='CBC')
    #
    # cw.decrypt_file('test_data/suai/suia.enc.bmp', 'test_data/suai/suia.dec.bmp', bmp=True, mode='CBC')


    # cw.encrypt_file('test_data/guap/guap.bmp', 'test_data/guap/guap.enc.bmp', bmp=True, mode='ECB')
    #
    # cw.decrypt_file('test_data/guap/guap.enc.bmp', 'test_data/guap/guap.dec.bmp', bmp=True, mode='ECB')

    cw.encrypt_file('test_data/guap/guap.bmp', 'test_data/guap/guap.enc.bmp', bmp=True, mode='CBC')

    cw.decrypt_file('test_data/guap/guap.enc.bmp', 'test_data/guap/guap.dec.bmp', bmp=True, mode='CBC')



