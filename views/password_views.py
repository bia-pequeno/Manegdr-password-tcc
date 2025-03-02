import os
import string
import secrets
import hashlib
import base64 
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

class FernetHasher:

    RANDOM_STRING_CHARS = string.ascii_lowercase + string.ascii_uppercase
    BASE_DIR = Path(__file__).resolve().parent.parent
    KEY_DIR = BASE_DIR / 'keys'

    def __init__(self, key):
        if not isinstance(key, bytes):
            key = key.encode()
        self.fernet = Fernet(key)
    
    @classmethod
    def _get_random_string(cls, length=25):
        return ''.join(secrets.choice(cls.RANDOM_STRING_CHARS) for _ in range(length))

    @classmethod
    def create_key(cls, archive=False):
        value = cls._get_random_string()
        hasher = hashlib.sha256(value.encode('utf-8')).digest()
        key = base64.b64encode(hasher)
        if archive:
            return key, cls.archive_key(key)
        return key

    @classmethod
    def archive_key(cls, key):
        try:
            if not cls.KEY_DIR.exists():
                os.makedirs(cls.KEY_DIR)
                print(f"Diretório {cls.KEY_DIR} criado.")  # Log para depuração

            file = 'key.key'
            while Path(cls.KEY_DIR / file).exists():
                file = f'key_{cls._get_random_string(length=5)}.key'

            print(f"Tentativa de salvar a chave em: {cls.KEY_DIR / file}")  # Log para depuração

            with open(cls.KEY_DIR / file, 'wb') as arq:
                arq.write(key)

            print(f"Chave armazenada em: {cls.KEY_DIR / file}")  # Log para depuração
            return cls.KEY_DIR / file
        except Exception as e:
            print(f"Erro ao tentar criar arquivo de chave: {e}")
        

    def encrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        encrypted_value = self.fernet.encrypt(value)
        print(f"Valor criptografado: {encrypted_value}")  # Log para depuração
        return encrypted_value

    def decrypt(self, value):
        if not isinstance(value, bytes):
            value = value.encode('utf-8')
        try:
            decrypted_value = self.fernet.decrypt(value).decode()
            print(f"Valor descriptografado: {decrypted_value}")  # Log para depuração
            return decrypted_value
        except InvalidToken:
            print(f"Falha ao descriptografar, token inválido para valor: {value}")  # Log para depuração
            return 'Token inválido'
# Verificação adicional para garantir que o diretório está correto
if not os.path.isdir(FernetHasher.KEY_DIR):
    print(f"Erro: Diretório {FernetHasher.KEY_DIR} não existe ou não é um diretório.")
else:
    print(f"Diretório {FernetHasher.KEY_DIR} verificado com sucesso.")