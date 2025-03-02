from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from model.password import Password
from views.password_views import FernetHasher

app = FastAPI(
        title="API de Gerenciador de Senhas",
        description="Essa API permite a criação, armazenamento seguro e gerenciamento de senhas. "
                    "Inclui funcionalidades como criptografia, consulta, atualização e exclusão de credenciais, "
                    "além de um gerador de senhas seguras.",
    version="1.0.0",
    contact={
        "name": "Beatriz",
        "email": "bia.2017pequeno@gmail.com",
    },
)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/create_key")
async def create_key():
    key = FernetHasher.create_key()
    return {"key": key.decode("utf-8")}

@app.post("/save_password")
async def save_password(request: Request):
    data = await request.json()
    domain = data['domain']
    password = data['password']
    key = data['key']
    fernet = FernetHasher(key)
    p1 = Password(domain=domain, password=fernet.encrypt(password).decode('utf-8'))

    p1.save()

    return {"status": "success"}

@app.post("/view_password")
async def view_password(request: Request):
    data = await request.json()
    domain = data['domain']
    key = data['key']
    
    # Garante que a chave passada está no formato correto (bytes)
    fernet = FernetHasher(key.encode('utf-8'))  # Converte a chave para bytes, se necessário
    data = Password.get()

    found_password = None
    for i in data:
        if domain in i['domain']:
            found_password = fernet.decrypt(i['password'])
            break
    return {"password": found_password}
