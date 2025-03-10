import sqlite3
import os

# Identificar se está em produção no Vercel
if os.getenv("VERCEL_ENV"):
    DB_PATH = "/tmp/passwords.db"  # No Vercel, usamos /tmp
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "passwords.db")  # Local

# Função para conectar ao banco de dados
def connect_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

# Função para criar a tabela de senhas, se não existir
def create_table():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT UNIQUE NOT NULL,
                encrypted_password TEXT NOT NULL,
                encryption_key TEXT NOT NULL
            )
        """)
        conn.commit()
        print(f"Tabela 'passwords' criada ou já existente no caminho: {DB_PATH}")  # Log para depuração
    except sqlite3.Error as e:
        print(f"Erro ao criar a tabela: {e}")
    finally:
        conn.close()

# Função para salvar ou atualizar a senha no banco de dados
def save_password_db(domain, encrypted_password, encryption_key):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO passwords (domain, encrypted_password, encryption_key) 
            VALUES (?, ?, ?)
            ON CONFLICT(domain) 
            DO UPDATE SET encrypted_password=excluded.encrypted_password, encryption_key=excluded.encryption_key
        """, (domain, encrypted_password, encryption_key))
        conn.commit()
        print(f"Senha salva para o domínio '{domain}'.")  # Log para depuração
    except sqlite3.Error as e:
        print(f"Erro ao salvar senha no banco: {e}")
    finally:
        conn.close()

# Função para recuperar a senha criptografada e a chave de encriptação pelo domínio
def get_password_db(domain):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT encrypted_password, encryption_key FROM passwords WHERE domain=?", (domain,))
        result = cursor.fetchone()
        print(f"Senha recuperada para o domínio '{domain}': {result}")  # Log para depuração
        return result
    except sqlite3.Error as e:
        print(f"Erro ao buscar senha no banco: {e}")
        return None
    finally:
        conn.close()

# Criar a tabela ao iniciar
create_table()
