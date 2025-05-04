import requests

turmas = [
    {
        "nome": "Turma A - 1 Ano",
        "professor_id": 1  # Relacionado ao primeiro professor (Dr. João Souza)
    },
    {
        "nome": "Turma B - 2 Ano",
        "professor_id": 2  # Relacionado ao segundo professor (Profa. Maria Oliveira)
    },
    {
        "nome": "Turma C - 3 Ano",
        "professor_id": 3  # Relacionado ao terceiro professor (Dr. Carlos Lima)
    }
]

url_turmas = "http://127.0.0.1:5000/turmas"

for turma in turmas:
    response = requests.post(url_turmas, json=turma)
    if response.status_code == 201:
        print(f"Turma '{turma['nome']}' criada com sucesso!")
    else:
        print(f"Erro ao criar turma '{turma['nome']}': {response.status_code} - {response.text}")
