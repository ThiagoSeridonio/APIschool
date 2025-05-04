import requests

# IDs das turmas que você quer deletar
ids_para_deletar_turmas = [1, 2, 3]  # Altere conforme necessário

url_base_turmas = "http://127.0.0.1:5000/turmas"

for turma_id in ids_para_deletar_turmas:
    url = f"{url_base_turmas}/{turma_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        print(f"Turma com ID {turma_id} deletada com sucesso!")
    else:
        print(f"Erro ao deletar turma com ID {turma_id}: {response.status_code} - {response.text}")
