from fastapi import APIRouter, HTTPException
from model.password import Password
from views.password_utils import FernetHasher

router = APIRouter()
hasher = FernetHasher()  # Instância do encriptador

@router.post("/save_password")
async def save_password_route(domain: str, password: str):
    encryption_key = hasher.create_key()  # Gerar chave para encriptação
    encrypted_password = hasher.encrypt(password)  # Criptografando a senha
    success = Password.save_to_db(domain, encrypted_password, encryption_key.decode())  # Salva a senha com chave
    
    if success:
        return {"message": "Senha salva com sucesso!"}
    else:
        raise HTTPException(status_code=500, detail="Erro ao salvar a senha.")

@router.get("/view_password")
async def view_password_route(domain: str):
    password_entry = Password.get_from_db(domain)

    if password_entry:
        encrypted_password, encryption_key = password_entry
        hasher = FernetHasher(encryption_key)  # Inicializa o FernetHasher com a chave armazenada
        decrypted_password = hasher.decrypt(encrypted_password)
        return {"domain": domain, "password": decrypted_password}
    else:
        raise HTTPException(status_code=404, detail="Senha não encontrada.")
