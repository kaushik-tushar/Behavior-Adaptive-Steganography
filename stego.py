from PIL import Image
import hashlib
import random
from crypto import encrypt_message, decrypt_message


# -------------------------------------------------
# PASSWORD BASED PIXEL SEQUENCE
# -------------------------------------------------
def get_pixel_sequence(width, height, password):
    seed = int(hashlib.sha256(password.encode()).hexdigest(), 16)
    rng = random.Random(seed)

    coords = [(x, y) for y in range(height) for x in range(width)]
    rng.shuffle(coords)
    return coords


# -------------------------------------------------
# STRING → BINARY
# -------------------------------------------------
def to_binary(data):
    return ''.join(format(ord(c), '08b') for c in data)


# -------------------------------------------------
# BINARY → STRING
# -------------------------------------------------
def from_binary(binary):
    chars = []
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) < 8:
            break
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)


# -------------------------------------------------
# EMBED MESSAGE (FINAL)
# -------------------------------------------------
def embed_message(image_path, secret_text, behavior=None, password="default123"):

    if behavior is None:
        behavior = {"risk_level": "medium"}

    # 🔐 Encrypt message
    encrypted = encrypt_message(secret_text)

    img = Image.open(image_path).convert("RGB")
    pixels = img.load()
    width, height = img.size

    # 🔥 Convert to binary
    binary_data = to_binary(encrypted)

    # 🔥 Add length header (32 bits)
    length = format(len(binary_data), '032b')
    binary = length + binary_data

    coords = get_pixel_sequence(width, height, password)

    risk = behavior.get("risk_level", "medium")
    step = {"low": 4, "medium": 2, "high": 1}.get(risk, 2)

    idx = 0

    for i in range(0, len(coords), step):
        if idx >= len(binary):
            break

        x, y = coords[i]
        r, g, b = pixels[x, y]

        # Embed in R channel only (stable)
        r = (r & ~1) | int(binary[idx])
        pixels[x, y] = (r, g, b)

        idx += 1

    # 🔥 Safety check
    if idx < len(binary):
        raise Exception("Image too small to hold data")

    output_path = image_path.rsplit(".", 1)[0] + "_stego.png"
    img.save(output_path, "PNG")

    return output_path


# -------------------------------------------------
# EXTRACT MESSAGE (FINAL)
# -------------------------------------------------
def extract_message(image_path, password="default123", behavior=None):

    if behavior is None:
        behavior = {"risk_level": "medium"}

    img = Image.open(image_path).convert("RGB")
    pixels = img.load()
    width, height = img.size

    coords = get_pixel_sequence(width, height, password)

    risk = behavior.get("risk_level", "medium")
    step = {"low": 4, "medium": 2, "high": 1}.get(risk, 2)

    binary = ""

    # 🔥 Extract bits
    for i in range(0, len(coords), step):
        x, y = coords[i]
        r, g, b = pixels[x, y]
        binary += str(r & 1)

    # 🔥 Get length (first 32 bits)
    length = int(binary[:32], 2)

    # 🔥 Extract actual data
    data_bits = binary[32:32 + length]

    encrypted = from_binary(data_bits)

    # 🔐 Decrypt message
    try:
        message = decrypt_message(encrypted)
    except Exception as e:
        raise Exception("Decryption failed: " + str(e))

    return message