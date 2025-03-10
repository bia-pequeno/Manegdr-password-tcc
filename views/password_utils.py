import os
import string
import secrets
import hashlib
import base64
import sqlite3
from pathlib import Path
from cryptography.fernet import Fernet, InvalidToken

class FernetHasher:
    RANDOM_STRING_CHARS = string.ascii_lowercase + string.ascii_uppercase
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_PATH = BASE_DIR / 'db' / 'passwords.db'  # Banco de dados SQLite

    def __init__(self, key=None):
        if key is None:
            key = self._get_or_create_key()  # Obtém a chave do banco
        if not isinstance(key, bytes):
            key = key.encode()
        self.fernet = Fernet(key)

    @classmethod
    def _get_random_string(cls, length=25):
        return ''.join(secrets.choice(cls.RANDOM_STRING_CHARS) for _ in range(length))

    @classmethod
    def create_key(cls):
        """Gera uma nova chave e salva no banco de dados."""
        value = cls._get_random_string()
        hasher = hashlib.sha256(value.encode('utf-8')).digest()
        key = base64.b64encode(hasher)

        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO keys (key_value) VALUES (?)
        """, (key.decode(),))
        conn.commit()
        conn.close()

        return key

    @classmethod
    def _get_or_create_key(cls):
        """Recupera a chave do banco ou cria uma nova se não existir."""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT key_value FROM keys ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if row:
            return row[0]  # Retorna a chave armazenada
        else:
            return cls.create_key()  # Cria uma nova chave e salva no banco

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

# Criação da tabela se não existir
def setup_database():
    conn = sqlite3.connect(FernetHasher.DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_value TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

setup_database()
