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

def calcular_media(aluno):
    notas = [aluno.get("nota_primeiro_semestre"), aluno.get("nota_segundo_semestre")]
    notas_validas = [n for n in notas if isinstance(n, (int, float))]
    return sum(notas_validas) / len(notas_validas) if notas_validas else None

def validar_aluno(novo_aluno):
    campos = ["nome", "data_nascimento", "nota_primeiro_semestre", "nota_segundo_semestre"]

    for campo in campos:
        if campo not in novo_aluno:
            return f"O campo '{campo}' é obrigatório.", 400

    if not validar_nome(novo_aluno["nome"]):
        return "O nome deve ser uma string válida sem caracteres especiais.", 400

    if not validar_data(novo_aluno["data_nascimento"]):
        return "A data de nascimento deve estar no formato YYYY-MM-DD.", 400

    try:
        novo_aluno["nota_primeiro_semestre"] = float(novo_aluno["nota_primeiro_semestre"])
        novo_aluno["nota_segundo_semestre"] = float(novo_aluno["nota_segundo_semestre"])
    except ValueError:
        return "As notas devem ser valores numéricos.", 400

    return None

def listar_alunos():
    return db.Database.load_data()["alunos"]

def buscar_aluno_por_id(id):
    alunos = listar_alunos()
    return next((a for a in alunos if a["id"] == id), None)

def adicionar_aluno(aluno):
    data = db.Database.load_data()
    aluno["id"] = db.Database.gerar_uuid()
    data["alunos"].append(aluno)
    db.Database.save_data(data)
    return aluno

def atualizar_aluno(id, dados):
    data = db.Database.load_data()
    for aluno in data["alunos"]:
        if aluno["id"] == id:
            aluno.update(dados)
            db.Database.save_data(data)
            return aluno
    return None

def remover_aluno(id):
    data = db.Database.load_data()
    alunos = data["alunos"]
    nova_lista = [a for a in alunos if a["id"] != id]
    if len(nova_lista) == len(alunos):
        return False
    data["alunos"] = nova_lista
    db.Database.save_data(data)
    return True
