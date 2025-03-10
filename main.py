from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from cryptography.fernet import Fernet
import json
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from db.database import save_password_db, get_password_db  # Importando as funções do banco de dados

app = FastAPI()

class PasswordData(BaseModel):
    password: str
    domain: str
    key: str

# Servindo arquivos estáticos da pasta "static"
app.mount("/static", StaticFiles(directory="static"), name="static")

# Rota para servir o arquivo HTML principal
@app.get("/", response_class=HTMLResponse)
async def read_index():
    file_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(file_path, "r") as f:
        return f.read()

# Classe para criar chave e criptografar/descriptografar senhas
class FernetHasher:
    def __init__(self, key=None):
        if key is None:
            self.key = Fernet.generate_key()  # Gera chave aleatória
        else:
            self.key = key.encode()  # Usa chave fornecida
        self.cipher = Fernet(self.key)

    def encrypt(self, password: str):
        return self.cipher.encrypt(password.encode())

    def decrypt(self, encrypted_password: bytes):
        return self.cipher.decrypt(encrypted_password).decode()

# Rota para gerar uma chave
@app.get("/create_key")
async def create_key():
    try:
        key = Fernet.generate_key()
        return {"key": key.decode()}  # Retorna a chave gerada
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro ao gerar chave.")

# Rota para salvar senha
@app.post("/save_password")
async def save_password(data: PasswordData):
    try:
        # Criptografando a senha
        hasher = FernetHasher(data.key)
        encrypted_password = hasher.encrypt(data.password)
        
        # Salvando a senha no banco de dados SQLite
        save_password_db(data.domain, encrypted_password, data.key)
        
        return {"message": "Senha salva com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar a senha: {str(e)}")

# Rota para visualizar senha
@app.get("/view_password")
async def view_password(domain: str, key: str):
    try:
        # Recuperando a senha criptografada do banco de dados
        result = get_password_db(domain)
        
        if result is None:
            raise HTTPException(status_code=404, detail="Senha não encontrada.")
        
        encrypted_password, stored_key = result
        if stored_key != key:
            raise HTTPException(status_code=400, detail="Chave incorreta.")
        
        # Descriptografando a senha
        hasher = FernetHasher(stored_key)
        password = hasher.decrypt(encrypted_password)
        
        return {"domain": domain, "password": password}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao recuperar a senha: {str(e)}")
