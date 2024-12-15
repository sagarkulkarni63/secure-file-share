import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.exceptions import InvalidKey

KEY = os.environ.get("FILE_ENCRYPTION_KEY", "a"*32).encode("utf-8")

def encrypt_data(data: bytes) -> bytes:
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(KEY), modes.CFB(iv))
    encryptor = cipher.encryptor()
    return iv + encryptor.update(data) + encryptor.finalize()

def decrypt_data(data: bytes) -> bytes:
    try:
        # Ensure data is long enough to extract IV
        if len(data) < 16:
            raise ValueError("Encrypted data is too short")

        # Extract IV from the first 16 bytes
        iv = data[:16]
        
        # Decrypt the rest of the data
        cipher = Cipher(algorithms.AES(KEY), modes.CFB(iv))
        decryptor = cipher.decryptor()
        
        # Decrypt and finalize
        decrypted_data = decryptor.update(data[16:]) + decryptor.finalize()
        
        return decrypted_data

    except InvalidKey:
        raise ValueError("Invalid encryption key")
    except Exception as e:
        # Log the specific error for debugging
        print(f"Decryption error: {e}")
        raise