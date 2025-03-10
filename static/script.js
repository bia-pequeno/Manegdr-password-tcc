function generateKey() {
    fetch('/create_key', {  // Alterado para '/create_key' para corresponder ao backend
        method: 'GET',  // Mudado para GET para corresponder ao método correto do backend
    })
    .then(response => response.json())
    .then(data => {
        console.log('Resposta do servidor:', data); // Log para depuração
        if (data.key) {
            document.getElementById('key').value = data.key;
            alert('Chave gerada com sucesso! Guarde-a bem para não perder suas senhas.');
        } else {
            alert('Erro: a chave não foi gerada corretamente.');
        }
    })
    .catch(error => {
        console.error('Erro ao gerar a chave:', error);
    });
}

document.getElementById('save-password-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const domain = document.getElementById('domain').value;
    const password = document.getElementById('password').value;
    const key = document.getElementById('key').value;  // Garantir que a chave seja enviada

    console.log(`Salvando senha para domínio: ${domain}`); // Log para depuração

    fetch('/save_password', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ domain, password, key }),  // Incluindo a chave na requisição
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert('Senha salva com sucesso!');
        } else {
            alert('Erro ao salvar a senha.');
        }
    })
    .catch(error => {
        console.error('Erro ao salvar a senha:', error);
    });
});

document.getElementById('view-password-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const domain = document.getElementById('view-domain').value;
    const key = document.getElementById('view-key').value;  // A chave é necessária para descriptografar a senha

    console.log(`Tentando recuperar senha para domínio: ${domain}`); // Log para depuração

    fetch(`/view_password?domain=${encodeURIComponent(domain)}&key=${encodeURIComponent(key)}`, {
        method: 'GET',
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
