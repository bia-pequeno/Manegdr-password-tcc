from datetime import datetime
from pathlib import Path
import sqlite3

class BaseModel:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_DIR = BASE_DIR / 'db'
    DB_PATH = DB_DIR / 'passwords.db'

    def __init__(self):
        self._create_table()  # Garante que a tabela existe ao instanciar a classe

    def _create_table(self):
        """Cria a tabela se não existir no banco de dados"""
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.__class__.__name__} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                create_at TEXT NOT NULL,
                expire INTEGER NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def save(self):
        """Salva os dados no banco de dados SQLite"""
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()

        cursor.execute(f"""
            INSERT INTO {self.__class__.__name__} (domain, password, create_at, expire) 
            VALUES (?, ?, ?, ?)
            ON CONFLICT(domain) DO UPDATE SET password=excluded.password, create_at=excluded.create_at, expire=excluded.expire
        """, (self.domain, self.password, self.create_at, self.expire))

        conn.commit()
        conn.close()

        print(f"Dados salvos: {self.__dict__}")  # Depuração

    @classmethod
    def get(cls):
        """Retorna todas as senhas salvas no banco"""
        conn = sqlite3.connect(cls.DB_PATH)
        cursor = conn.cursor()
        cursor.execute(f"SELECT domain, password, create_at, expire FROM {cls.__name__}")
        rows = cursor.fetchall()
        conn.close()

        atributos = ["domain", "password", "create_at", "expire"]
        results = [dict(zip(atributos, row)) for row in rows]

        return results

class Password(BaseModel):
    def __init__(self, domain=None, password=None, expire=False):
        super().__init__()  # Chama o construtor da classe BaseModel
        self.domain = domain
        self.password = password
        self.create_at = datetime.now().isoformat()
        self.expire = 1 if expire else 0
