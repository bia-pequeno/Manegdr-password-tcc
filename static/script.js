function generateKey() {
    fetch('/create_key', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        console.log('Resposta do servidor:', data); // Verifica o retorno da API
        if (data.key) {
            document.getElementById('key').value = data.key;
            alert('Chave gerada com sucesso, guarde-a bem para não perder suas senhas!');
        } else {
            alert('Erro: a chave não foi gerada corretamente.');
        }
    })
    .catch(error => {
        console.error('Erro ao gerar a chave:', error);
    });
};

document.getElementById('save-password-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const domain = document.getElementById('domain').value;
    const password = document.getElementById('password').value;
    const key = document.getElementById('key').value;
    
    console.log(`Salvando senha para domínio: ${domain} com a chave: ${key}`);  // Log para depuração

    fetch('/save_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ domain, password, key }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Senha salva com sucesso!');
        }
    })
    .catch(error => {
        console.error('Erro ao salvar a senha:', error);
    });
});

document.getElementById('view-password-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const domain = document.getElementById('view-domain').value;
    const key = document.getElementById('view-key').value;
    
    console.log(`Tentando recuperar senha para domínio: ${domain} com a chave: ${key}`);  // Log para depuração

    fetch('/view_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ domain, key }),
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('password-result');
        if (data.password) {
            resultDiv.textContent = `Sua senha: ${data.password}`;
        } else {
            resultDiv.textContent = 'Nenhuma senha encontrada para esse domínio.';
        }
    })
    .catch(error => {
        console.error('Erro ao recuperar a senha:', error);
    });
});
