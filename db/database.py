import sqlite3
import os

# Caminho do banco de dados
DB_PATH = os.path.join(os.path.dirname(__file__), "passwords.db")

# Função para conectar ao banco de dados
def connect_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

# Função para criar a tabela de senhas, se não existir
def create_table():
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
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro ao salvar no banco: {e}")


# Função para recuperar a senha criptografada e a chave de encriptação pelo domínio
def get_password_db(domain):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT encrypted_password, encryption_key FROM passwords WHERE domain=?", (domain,))
    result = cursor.fetchone()
    conn.close()
    return result

# Chama a função para garantir que a tabela foi criada ao iniciar o app
create_table()
