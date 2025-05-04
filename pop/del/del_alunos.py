import requests

# IDs dos alunos que você quer deletar
ids_para_deletar = [1, 2, 3]  # Altere conforme necessário

url_base = "http://127.0.0.1:5000/alunos"

for aluno_id in ids_para_deletar:
    url = f"{url_base}/{aluno_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        print(f"Aluno com ID {aluno_id} deletado com sucesso!")
    else:
        print(f"Erro ao deletar aluno com ID {aluno_id}: {response.status_code} - {response.text}")
