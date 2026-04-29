import base64
import hashlib
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

# 🔐 Fixed password (you can later make it dynamic via user input)
SECRET_KEY = hashlib.sha256(b"default123").digest()


def encrypt_message(message):
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC)

    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))

    # Combine IV + ciphertext
    encrypted = cipher.iv + ciphertext

    # Encode to base64 string
    return base64.b64encode(encrypted).decode()


def decrypt_message(encrypted_message):
    raw = base64.b64decode(encrypted_message)

    iv = raw[:16]
    ciphertext = raw[16:]

    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv=iv)

    decrypted = unpad(cipher.decrypt(ciphertext), AES.block_size)

    return decrypted.decode()
