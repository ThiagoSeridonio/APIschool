import re
import database as db

def validar_nome(nome):
    return isinstance(nome, str) and re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", nome)

def validar_turma(turma):
    if not validar_nome(turma.get("nome", "")):
        return "Nome da turma inválido. Não use caracteres especiais.", 400
    if not isinstance(turma.get("turno"), str) or not turma["turno"].strip():
        return "Turno inválido. Deve ser uma string não vazia.", 400
    if not isinstance(turma.get("capacidade"), int) or turma["capacidade"] <= 0:
        return "Capacidade inválida. Deve ser um número inteiro positivo.", 400
    return None

def listar_turmas():
    return db.Database.load_data()["turmas"]

def buscar_turma_por_id(id):
    turmas = listar_turmas()
    return next((t for t in turmas if t["id"] == id), None)

def adicionar_turma(turma):
    data = db.Database.load_data()
    turma["id"] = db.Database.gerar_uuid()
    data["turmas"].append(turma)
    db.Database.save_data(data)
    return turma

def atualizar_turma(id, dados):
    data = db.Database.load_data()
    for turma in data["turmas"]:
        if turma["id"] == id:
            turma.update(dados)
            db.Database.save_data(data)
            return turma
    return None

def remover_turma(id):
    data = db.Database.load_data()
    turmas = data["turmas"]
    nova_lista = [t for t in turmas if t["id"] != id]
    if len(nova_lista) == len(turmas):
        return False
    data["turmas"] = nova_lista
    db.Database.save_data(data)
    return True
