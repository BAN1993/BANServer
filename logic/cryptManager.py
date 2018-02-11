#coding: utf8

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import hashlib
import logging

class cryptManager(object):
    m_AES_key = None
    m_AES_mode = None
    m_AES_hadKey = False

    def init(self, conf):
        self.m_AES_key = str(conf.get("serverConfig", "aeskey"))
        if len(self.m_AES_key) != 16:
            raise Exception("crypt key len must be 16")
        self.m_AES_mode = AES.MODE_CBC
        self.m_AES_hadKey = True

    # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
    def encryptAES(self, text):
        if not self.m_AES_hadKey or not self.m_AES_key:
            logging.error("Key is None")
            return
        cryptor = AES.new(self.m_AES_key, self.m_AES_mode, self.m_AES_key)
        # 这里密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度.目前AES-128足够用
        length = 16
        count = len(text)

        add = 0
        if (count % length) != 0:
            add = length - (count % length)
        text = text + ('\0' * add)

        ciphertext = cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(ciphertext)

    # 解密后，去掉补足的空格用strip() 去掉
    def decryptAES(self, text):
        if not self.m_AES_hadKey or not self.m_AES_key:
            logging.error("Key is None")
            return
        cryptor = AES.new(self.m_AES_key, self.m_AES_mode, self.m_AES_key)
        plain_text = cryptor.decrypt(a2b_hex(text))
        return plain_text.rstrip('\0')

    def md5(self, text):
        return hashlib.md5(str(text)).hexdigest()

gCrypt = cryptManager()