import sys, os
import base64
sys.path.append(os.path.abspath(os.curdir))
from model.password import Password
from views.password_views import FernetHasher

def convert_key(key):
    if isinstance(key, str):
        if len(key) != 32:
            key = base64.urlsafe_b64encode(base64.b64decode(key))
        key = key.encode()
    return key

def handle_save_password(key=None, domain=None, password=None):
    if key is None:
        if len(Password.get() or []) == 0:
            key, path = FernetHasher.create_key(archive=True)
            return 'Sua chave foi criada, salve-a com cuidado caso a perca não poderá recuperar suas senhas.'
        else:
            key = input('Digite sua chave usada para criptografia, use sempre a mesma chave: ')
        domain = input('Domínio: ')
        password = input('Digite a senha: ')
    key = convert_key(key)
    fernet = FernetHasher(key)
    p1 = Password(domain=domain, password=fernet.encrypt(password).decode('utf-8'))
    p1.save()
    return 'Senha salva com sucesso!'

def handle_view_password(domain=None, key=None):
    if domain is None or key is None:
        domain = input('Domínio: ')
        key = input('Chave: ')
    key = convert_key(key)
    fernet = FernetHasher(key)
    data = Password.get()
    found_password = None
    
    for i in data:
        if domain in i['domain']:
            found_password = fernet.decrypt(i['password'])
            break
    if found_password:
        return found_password, 'Sua senha é:'
    return None, 'Nenhuma senha encontrada para esse domínio.'

# Função original de templates.py (mantendo a estrutura)
if __name__ == '__main__':
    action = input('Digite 1 para salvar uma nova senha ou 2 para ver uma determinada senha: ')
    match action:
        case '1':
            print(handle_save_password())
        case '2':
            password, message = handle_view_password()
            if password:
                print(f'Sua senha: {password}')
            else:
                print(message)
