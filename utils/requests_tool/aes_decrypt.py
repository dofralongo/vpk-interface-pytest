# -*- coding: UTF-8 -*-
from __future__ import print_function
import base64
from Crypto.Cipher import AES
from hashlib import sha256 as sha
from threading import Lock

import binascii


cipher = None
cipher_lock = Lock()


def pad(text, with_char="pad_length"):
    # print("before padding: {}".format(text))
    tmp = text  # .encode('UTF-8')
    count = len(tmp)
    pad_count = (AES.block_size - (count % AES.block_size)) % AES.block_size if count != 0 \
        else AES.block_size
    # print('pad_count: {}'.format(pad_count))
    if with_char == "pad_length":
        text_padded = tmp + bytes(chr(pad_count) * pad_count, "ascii")
    else:
        text_padded = tmp + (with_char * pad_count)
    return text_padded


def unpad(text, with_char="pad_length"):
    # print("before unpadding: {}".format(binascii.b2a_hex(text)))
    tmp = bytes(text)
    if with_char == "pad_length":
        n_padding = ord(tmp[-1])
        if 0 < n_padding <= 16:
            t_len = len(tmp)
            is_padded = True
            for i in range(t_len-n_padding, t_len):
                if ord(tmp[i]) != n_padding:
                    is_padded = False
                    break

            if is_padded:
                print("padding length: {}".format(ord(tmp[-1])))
                tmp = tmp[:-n_padding]
    else:
        tmp = tmp.rstrip(with_char)
    return tmp


def gen_cipher_AES_ECB_sha256(psk, mode):         #万家的算法，使用ECB模式，先做256，再截取前16位
    global cipher
    # b64_psk = base64.encodestring(psk)
    if cipher is not None:
        return
    cipher_lock.acquire()
    hash_psk = binascii.b2a_hex(sha(psk).digest())[0:16]
    # print('psk sha256: {}'.format(binascii.b2a_hex(hash_psk)))
    if mode == AES.MODE_ECB:
        cipher = AES.new(hash_psk, AES.MODE_ECB)
        cipher_lock.release()
    else:
        cipher_lock.release()
        raise ValueError("AES mode {} is not supported now".format(mode))


gen_cipher = gen_cipher_AES_ECB_sha256


def gen_cipher_AES_CFB(psk, iv, segment_size=128, padding=False, with_char="pad_length"):
    global cipher
    psk = bytes(psk,"utf-8")
    iv = bytes(iv, "utf-8")
    if cipher is not None:
        return
    cipher_lock.acquire()   #多进程用不上
    if padding:
        t_psk = pad(psk)
        t_iv = pad(iv)
    else:
        t_psk = psk
        t_iv = iv
    cipher = AES.new(t_psk, AES.MODE_CFB, IV=t_iv, segment_size=segment_size)
    cipher_lock.release()    #多进程不用


def encrypt(plain_text, padding=False, with_char="pad_length"):     #加密
    global cipher
    # cyphered -> base64
    plain_text = bytes(str(plain_text), "utf-8")
    text = pad(plain_text, with_char=with_char) if padding else plain_text
    tmp = cipher.encrypt(text)
    ciphered = base64.encodebytes(tmp)   #编码
    # print(cipher)
    cipher = None
    # print(cipher)
    return ciphered


def decrypt(ciphered_text, padding=True, with_char="pad_length"):
    global cipher
    tmp = base64.decodebytes(ciphered_text+b'\n')      #解码
    plain_text = unpad(cipher.decrypt(tmp), with_char=with_char) if padding else cipher.decrypt(tmp)
    return plain_text


if __name__ == '__main__':
    # key = 'secret key for symmetrical encryption'
    # text = "12345678"
    # print('Orig: {}'.format(text))
    # gen_cipher_AES_ECB_sha256(key, 'ECB')
    # encrypted_text = encrypt(text).strip()
    # print('Encrypted: {}'.format(encrypted_text))
    # decrypted_text = decrypt(encrypted_text)
    # print('Decrypted: {}'.format(decrypted_text))
    # assert decrypted_text == text

    key = b'hi,gohigh.IoTHub'
    iv = b'hi,gohigh.IoTHub'
    text_orig = '123456'
    # text = bytes(text_orig,"utf-8")
    print('Orig: {}'.format(text_orig))  #原始文本
    gen_cipher_AES_CFB(key, iv, segment_size=128, padding=True)    
    encrypted_text = encrypt(text_orig, padding=False).strip()
    print('Encrypted: {}'.format(str(encrypted_text, encoding="utf-8")))   #打印密文
    cipher = None
    gen_cipher_AES_CFB(key, iv, segment_size=128, padding=True)
    decrypted_text = decrypt(encrypted_text, padding=False)
    print('Decrypted: {}'.format(decrypted_text))   #解密后的密文
    assert decrypted_text == text_orig
