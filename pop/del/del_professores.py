import requests

# IDs dos professores que você quer deletar
ids_para_deletar_professores = [1, 2, 3]  # Altere conforme necessário

url_base_professores = "http://127.0.0.1:5000/professores"

for professor_id in ids_para_deletar_professores:
    url = f"{url_base_professores}/{professor_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        print(f"Professor com ID {professor_id} deletado com sucesso!")
    else:
        print(f"Erro ao deletar professor com ID {professor_id}: {response.status_code} - {response.text}")
