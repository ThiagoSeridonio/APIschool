import requests

professores = [
    {
        "nome": "Dr. Joao Souza",
        "email": "joao.souza@example.com",
        "data_nascimento": "12/05/1980",
        "disciplina": "Matematica",
        "salario": 3500.75
    },
    {
        "nome": "Profa. Maria Oliveira",
        "email": "maria.oliveira@example.com",
        "data_nascimento": "22/08/1985",
        "disciplina": "Fisica",
        "salario": 4000.50
    },
    {
        "nome": "Dr. Carlos Lima",
        "email": "carlos.lima@example.com",
        "data_nascimento": "18/11/1978",
        "disciplina": "Quimica",
        "salario": 3800.00
    }
]

url_professores = "http://127.0.0.1:5000/professores"

for professor in professores:
    response = requests.post(url_professores, json=professor)
    if response.status_code == 201:
        print(f"Professor '{professor['nome']}' criado com sucesso!")
    else:
        print(f"Erro ao criar professor '{professor['nome']}': {response.status_code} - {response.text}")
