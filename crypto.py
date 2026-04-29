import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# 🔐 Fixed password (can upgrade later)
SECRET_KEY = hashlib.sha256(b"default123").digest()


def encrypt_message(message):
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC)

    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))

    # 🔥 prepend IV with ciphertext
    encrypted = cipher.iv + ciphertext

    # convert to string
    return base64.b64encode(encrypted).decode()


def decrypt_message(encrypted_message):
    raw = base64.b64decode(encrypted_message)

    iv = raw[:16]
    ciphertext = raw[16:]

    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv=iv)

    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)

    return decrypted.decode()