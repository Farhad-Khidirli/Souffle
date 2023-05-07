from Crypto.Protocol.KDF import scrypt
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def encrypt(_data, _key):
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(_key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(_data, AES.block_size))


def decrypt(_data, _key):
    iv = _data[:AES.block_size]
    ciphertext = _data[AES.block_size:]
    cipher = AES.new(_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), AES.block_size)


def generate_key(_passphrase, _salt, _len, _r, _p):
    encryption_key = scrypt(
        password=_passphrase.encode(),
        salt=_salt,
        key_len=_len,
        N=2 ** 20,
        r=_r,
        p=_p
    )
    return encryption_key


def init_key(keyword, _salt):
    # salt = get_random_bytes(16)
    encryption_key = generate_key(keyword, _salt, 32, 8, 1)
    return encryption_key

