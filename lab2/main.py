from lab2new import JeffersonCylinder2BlockCipher as JC, add_text_to_image
from lab2new import CryptoWrapper as CW

def process_BMP(mode, filename_template, cw):
    file_source = filename_template.format(suffix='')
    filename_template = filename_template.format(suffix='.%s{suffix}' % mode)
    file_enc = filename_template.format(suffix='.enc')
    file_dec = filename_template.format(suffix='.dec')
    file_bad_enc = filename_template.format(suffix='.bad.enc')
    file_bad_dec = filename_template.format(suffix='.bad.dec')

    # cw.encrypt_file(file_source, file_enc, True, mode)
    # cw.decrypt_file(file_enc, file_dec, True, mode)

    # add_text_to_image(file_enc, file_bad_enc, "TEXT")

    cw.decrypt_file(file_bad_enc, file_bad_dec, True, mode)

if __name__ == '__main__':
    block_size = 4
    round_count = 1
    # disks = JC.generate_disks(block_size)
    # JC.save_disks(disks)
    disks = JC.load_disks()
    jf = JC(disks, block_size, round_count=round_count)
    # jf.encrypt_file('hello.txt')
    #
    # jf.decrypt_file('hello.txt.enc')
    cw = CW(jf)
    # cw.encrypt_file('test_data/mars/mars2.png')
    #
    # cw.decrypt_file('test_data/mars/mars2.png.enc', 'test_data/mars/mars2.dec.png')


    filename_template = "test_data/suai/suai{suffix}.bmp"

    process_BMP('CBC', filename_template, cw)

    filename_template = "test_data/guap/guap{suffix}.bmp"

    process_BMP('CBC', filename_template, cw)
    # file_source = filename_template.format(suffix='')
    # file_enc = filename_template.format(suffix='.enc')
    # file_dec = filename_template.format(suffix='.dec')
    #
    # cw.encrypt_file(file_source, file_enc, bmp=True, mode='CBC')
    #
    #
    # cw.decrypt_file(file_enc, file_dec, bmp=True, mode='CBC')
    # cw.decrypt_file('test_data/suai/suia.enc.bad.bmp', 'test_data/suai/suia.dec.bmp', bmp=True, mode='CBC')


    # cw.encrypt_file('test_data/guap/guap.bmp', 'test_data/guap/guap.enc.bmp', bmp=True, mode='ECB')
    #
    # cw.decrypt_file('test_data/guap/guap.enc.bmp', 'test_data/guap/guap.dec.bmp', bmp=True, mode='ECB')

    # cw.encrypt_file('test_data/guap/guap.bmp', 'test_data/guap/guap.enc.bmp', bmp=True, mode='CBC')
    #
    # cw.decrypt_file('test_data/guap/guap.enc.bmp', 'test_data/guap/guap.dec.bmp', bmp=True, mode='CBC')



