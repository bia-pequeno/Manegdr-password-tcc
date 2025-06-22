# Gerenciador de Senhas

O Gerenciador de Senhas é um software que inclui uma API desenvolvida em FastAPI para facilitar o armazenamento, a criptografia e a gestão de senhas de forma segura. Ele oferece uma interface para que usuários possam cadastrar, atualizar e recuperar senhas protegidas por um sistema de criptografia baseado na biblioteca Cryptography.

## Funcionalidades

- **Cadastro de Senha:** Permite armazenar senhas criptografadas para diferentes domínios.
- **Consulta de Senha:** Recupera uma senha armazenada com segurança.
- **Atualização de Senha:** Permite modificar uma senha existente.
- **Exclusão de Senha:** Remove uma senha do sistema.
- **Gerador de Senhas:** Gera senhas seguras aleatórias.

## Tecnologias Utilizadas

- **FastAPI:** Framework web para construção de APIs.
- **Cryptography (Fernet):** Para criptografar e descriptografar senhas.
- **Pydantic:** Biblioteca para validação de dados.
- **Uvicorn:** Servidor ASGI para execução da API.

## Acesse o site aqui
- https://manegdr-password-tcc.vercel.app/

## 🖼️ Demonstrações

### 💻 Visualização Desktop

<img src="https://raw.githubusercontent.com/bia-pequeno/Manegdr-password-tcc/main/assets/desktop.png" alt="Tela Desktop" width="700"/>

### 📱 Visualização Mobile

<img src="https://raw.githubusercontent.com/bia-pequeno/Manegdr-password-tcc/main/assets/mobile.png" alt="Tela Mobile" width="300"/>


### Estrutura do Projeto

```
/managedr-password
├── /db
│   ├── Password.txt 
├── /keys                   
├── /model
│   ├── password.py         
├── /static
│   ├── script.js
│   ├── styles.css
├── /templates
│   ├── index.html
│   ├── templates.py
├── /views
│   ├── password_views.py
├── main.py
├── requirements.txt  
└── vercel.json   
```

### Requisitos

- **Python 3.7 ou superior**
- **FastAPI**
- **Uvicorn**
- **Cryptography**

### Instalação

1. **Clone este repositório:**

   ```bash
   git clone https://github.com/bia-pequeno/Manegdr-password-tcc.git
   ```

2. **Navegue até o diretório do projeto:**

   ```bash
   cd Manegdr-password-tcc
   ```

3. **Crie um Virtual Environment:**

   ```bash
   python -m venv myenv
   ```

4. **Ative o ambiente virtual:**

   - No Windows:
     ```bash
     myenv\Scripts\activate
     ```
   - No Linux/Mac:
     ```bash
     source myenv/bin/activate
     ```

5. **Instale as dependências:**

   ```bash
   pip install fastapi uvicorn cryptography
   ```
