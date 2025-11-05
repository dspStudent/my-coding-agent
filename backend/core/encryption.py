from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os
from dotenv import load_dotenv

load_dotenv()

ENCRYPTION_KEY = base64.b64decode(os.getenv("ENCRYPTION_KEY"))

def encrypt(plain_text: str) -> str:
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_GCM)
    cipher_text, tag = cipher.encrypt_and_digest(plain_text.encode('utf-8'))
    return base64.b64encode(cipher.nonce + tag + cipher_text).decode('utf-8')

def decrypt(cipher_text: str) -> str:
    decoded_text = base64.b64decode(cipher_text)
    nonce = decoded_text[:16]
    tag = decoded_text[16:32]
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_GCM, nonce=nonce)
    plain_text = cipher.decrypt_and_verify(decoded_text[32:], tag)
    return plain_text.decode('utf-8')
