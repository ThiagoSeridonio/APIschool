import re
import datetime
import database as db


def validar_nome(nome):
    return isinstance(nome, str) and re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", nome)

def validar_data(data):
    return isinstance(data, str) and re.match(r"^\d{4}-\d{2}-\d{2}$", data)

def calcular_idade(data_nascimento):
    if not validar_data(data_nascimento):
        return None
    ano_nascimento = int(data_nascimento.split("-")[0])
    return datetime.datetime.now().year - ano_nascimento

def listar_professores():
    data = db.Database.load_data()
    for professor in data["professores"]:
        professor["idade"] = calcular_idade(professor.get("data_nascimento", ""))
    return data["professores"]

def buscar_professor_por_id(prof_id):
    data = db.Database.load_data()
    for professor in data["professores"]:
        if professor["id"] == prof_id:
            return professor
    return None

def adicionar_professor(novo_professor):
    data = db.Database.load_data()
    novo_professor["id"] = db.Database.gerar_uuid()
    data["professores"].append(novo_professor)
    db.Database.save_data(data)
    return novo_professor

def atualizar_professor(prof_id, novos_dados):
    data = db.Database.load_data()
    for professor in data["professores"]:
        if professor["id"] == prof_id:
            professor.update(novos_dados)
            db.Database.save_data(data)
            return professor
    return None

def remover_professor(prof_id):
    data = db.Database.load_data()
    professores = data["professores"]
    novo_lista = [p for p in professores if p["id"] != prof_id]
    if len(novo_lista) == len(professores):
        return False
    data["professores"] = novo_lista
    db.Database.save_data(data)
    return True
