from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

def aes_encrypt(message, key):
    # 生成随机的初始化向量

    # 创建 Cipher 对象并使用 CBC 模式
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # 填充消息为块大小的倍数
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message.encode()) + padder.finalize()

    # 加密并返回 IV + 密文
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext


def aes_decrypt(ciphertext, key):
    # 提取 IV 和密文
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]

    # 创建 Cipher 对象并使用 CBC 模式
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # 解密并移除填充
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    return unpadded_data.decode()


if __name__ == "__main__":
    # 生成随机的 256 位密钥
    # key = os.urandom(32)
    # iv = os.urandom(16)
    # print(key)
    # print(iv)
    key = b'x\x95\xd9O\x82x\xbb\xabX}\xce\xd6\xaf\xa8\x06_\xaf\xe4Q\xbdH\x85\xf6\x81`x\xc3\x00\xd5\x90|\xed'
    iv = b'm(m\xe3\xb1X\xfb\xffW\x8fw,\xe3\x19\x0eM'
    # 要加密的消息
    message = '今天是2024-01-03'

    # 加密消息
    encrypted_message = aes_encrypt(message, key)
    print(f"Encrypted message: {encrypted_message}")


    # 解密消息
    decrypted_message = aes_decrypt(encrypted_message, key)
    print(f"Decrypted message: {decrypted_message}")