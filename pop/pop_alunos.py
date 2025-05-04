import requests

alunos = [
    {
        "nome": "Joao Silva",
        "data_nascimento": "10/01/2000",
        "nota1": 8.5,
        "nota2": 7.0
    },
    {
        "nome": "Maria Oliveira",
        "data_nascimento": "15/07/1998",
        "nota1": 9.0,
        "nota2": 9.5
    },
    {
        "nome": "Carlos Lima",
        "data_nascimento": "22/03/1995",
        "nota1": 6.0,
        "nota2": 5.5
    }
]

url = "http://127.0.0.1:5000/alunos"

for aluno in alunos:
    response = requests.post(url, json=aluno)
    if response.status_code == 201:
        print(f"Aluno '{aluno['nome']}' criado com sucesso!")
    else:
        print(f"Erro ao criar aluno '{aluno['nome']}': {response.status_code} - {response.text}")
