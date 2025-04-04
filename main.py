from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from cryptography.fernet import Fernet
from db.database import save_password_db, get_password_db
import os
from db.database import connect_db
import sqlite3


app = FastAPI()

if os.getenv("VERCEL_ENV"):
    print("Arquivos no diretório /tmp:", os.listdir("/tmp"))  # Log para listar os arquivos no /tmp

# Modelos
class PasswordData(BaseModel):
    password: str
    domain: str
    key: str

# Servindo arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Rota para servir o HTML principal
@app.get("/", response_class=HTMLResponse)
async def read_index():
    file_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(file_path, "r") as f:
        return f.read()

# Classe para lidar com criptografia
class FernetHasher:
    def __init__(self, key=None):
        if key is None:
            self.key = Fernet.generate_key()  # Chave aleatória
        else:
            self.key = key.encode()  # Usa chave fornecida
        self.cipher = Fernet(self.key)

    def encrypt(self, password: str):
        return self.cipher.encrypt(password.encode())

    def decrypt(self, encrypted_password: bytes):
        return self.cipher.decrypt(encrypted_password).decode()

# Rota para gerar chave
@app.get("/create_key")
async def create_key():
    try:
        key = Fernet.generate_key()
        return {"key": key.decode()}  # Retorna a chave gerada
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar chave: {e}")

# Rota para salvar senha
@app.post("/save_password")
async def save_password(data: PasswordData):
    try:
        # Criptografando a senha
        hasher = FernetHasher(data.key)
        encrypted_password = hasher.encrypt(data.password)

        # Salvando a senha no banco
        save_password_db(data.domain, encrypted_password, data.key)

        return {"message": "Senha salva com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar a senha: {e}")

# Rota para visualizar senha
@app.get("/view_password")
async def view_password(domain: str, key: str):
    try:
        # Recuperar dados do banco
        result = get_password_db(domain)
        if result is None:
            raise HTTPException(status_code=404, detail="Senha não encontrada.")
        
        encrypted_password, stored_key = result
        if stored_key != key:
            raise HTTPException(status_code=400, detail="Chave incorreta.")
        
        # Descriptografar senha
        hasher = FernetHasher(stored_key)
        password = hasher.decrypt(encrypted_password)
        return {"domain": domain, "password": password}
    except sqlite3.Error as e:
        print(f"Erro no banco de dados: {e}")
        raise HTTPException(status_code=500, detail="Erro no banco de dados.")
    except Exception as e:
        print(f"Erro geral: {e}")  # Log para depuração
        raise HTTPException(status_code=500, detail="Erro interno no servidor.")

@app.get("/check_db")
async def check_db():
    if os.path.exists("/tmp/passwords.db"):
        return {"message": "Banco de dados encontrado no Vercel", "path": "/tmp/passwords.db"}
    else:
        return {"message": "Banco de dados NÃO encontrado", "path": "/tmp"}

@app.get("/view_all_domains")
async def view_all_domains():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT domain FROM passwords")  # Busca apenas os domínios
        domains = cursor.fetchall()
        return {"domains": [row[0] for row in domains]}  # Retorna a lista de domínios
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar domínios: {e}")
    finally:
        conn.close()

