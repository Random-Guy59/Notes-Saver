'''Encryption and hashing for Notes Saver'''

from cryptography.fernet import Fernet
import json

def load_key() -> str:
    '''Loads encryption key for fernet. If not available, creates one'''
    try:
        with open('secret.key', 'rb') as file:
            return file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open('secret.key', 'wb') as file:
            file.write(key)
        return key

fernet = Fernet(load_key())

def encrypt_json(obj: list) -> str:
    '''Dumps the obj and then encrypts it.'''
    return fernet.encrypt(json.dumps(obj).encode())

def decrypt_json(obj: str) -> list:
    '''Decrypts the obj and then loads it.'''
    return json.loads(fernet.decrypt(obj).decode())