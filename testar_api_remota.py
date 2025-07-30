import requests

API_URL = 'https://cadastro-marcas.onrender.com'

def listar_marcas():
    res = requests.get(f'{API_URL}/marcas')
    print('Status:', res.status_code)
    print('Marcas:', res.json())

def detalhar_marca(numero_processo):
    res = requests.get(f'{API_URL}/marca/{numero_processo}')
    print('Status:', res.status_code)
    if res.ok:
        print('Marca:', res.json())
    else:
        print('Erro:', res.text)

def cadastrar_marca():
    dados = {
        'numero_processo': '123456',
        'nome': 'Marca Teste',
        'titular': 'Titular Teste',
        'classe': 'Classe Teste',
        'status': 'Ativo',
        'especificacoes': 'Especificações Teste',
        'observacoes': 'Observações Teste',
        'vendedor': 'Vendedor Teste',
        'comprador': 'Comprador Teste',
    }
    arquivos = {
        'arquivo': open('teste.txt', 'rb')  # coloque um arquivo 'teste.txt' no mesmo diretório
    }

    res = requests.post(f'{API_URL}/marca', data=dados, files=arquivos)
    print('Status:', res.status_code)
    print('Resposta:', res.json())

def atualizar_marca():
    dados = {
        'nome': 'Marca Teste Atualizada',
        'status': 'Inativo',
    }
    res = requests.put(f'{API_URL}/marca/123456', data=dados)
    print('Status:', res.status_code)
    print('Resposta:', res.json())

def deletar_marca():
    res = requests.delete(f'{API_URL}/marca/123456')
    print('Status:', res.status_code)
    print('Resposta:', res.json())

if __name__ == '__main__':
    listar_marcas()
    cadastrar_marca()
    detalhar_marca('123456')
    atualizar_marca()
    detalhar_marca('123456')
    deletar_marca()
    listar_marcas()
