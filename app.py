import datetime
from flask import Flask, jsonify, request
import database as db
import re

app = Flask(__name__)

def validar_aluno(novo_aluno):
    """Função para validar os dados do aluno"""

    campos_obrigatorios = ["nome", "data_nascimento", "nota_primeiro_semestre", "nota_segundo_semestre"]

    for campo in campos_obrigatorios:
        if campo not in novo_aluno:
            return f"O campo '{campo}' é obrigatório.", 400

    if not isinstance(novo_aluno["nome"], str) or not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", novo_aluno["nome"]):
        return "O nome deve ser uma string válida sem caracteres especiais.", 400

    if not isinstance(novo_aluno["data_nascimento"], str) or not re.match(r"^\d{4}-\d{2}-\d{2}$", novo_aluno["data_nascimento"]):
        return "A data de nascimento deve estar no formato YYYY-MM-DD.", 400

    try:
        novo_aluno["nota_primeiro_semestre"] = float(novo_aluno["nota_primeiro_semestre"])
        novo_aluno["nota_segundo_semestre"] = float(novo_aluno["nota_segundo_semestre"])
    except ValueError:
        return "As notas devem ser valores numéricos.", 400

    return None  

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

@app.route("/professores", methods=["GET"])
def get_professores():
    data = db.Database.load_data()
    for professor in data["professores"]:
        professor["idade"] = calcular_idade(professor.get("data_nascimento", ""))
    return jsonify(data["professores"])

@app.route("/professores/<string:id>", methods=["GET"])
def get_professor(id):
    data = db.Database.load_data()
    for professor in data["professores"]:
        if professor["id"] == id:
            return jsonify(professor)
    return jsonify({"erro": "Professor não encontrado"}), 404

@app.route("/professores", methods=["POST"])
def post_professor():
    data = db.Database.load_data()
    novo_professor = request.json

    if not validar_nome(novo_professor.get("nome")):
        return jsonify({"erro": "Nome inválido. Não use caracteres especiais."}), 400
    if not validar_data(novo_professor.get("data_nascimento")):
        return jsonify({"erro": "Data de nascimento inválida. Use o formato YYYY-MM-DD."}), 400
    if not isinstance(novo_professor.get("disciplina"), str) or not novo_professor["disciplina"].strip():
        return jsonify({"erro": "Disciplina inválida. Deve ser uma string não vazia."}), 400
    if not isinstance(novo_professor.get("salario"), (float, int)):
        return jsonify({"erro": "Salário inválido. Deve ser um número."}), 400

    novo_professor["id"] = db.Database.gerar_uuid()
    data["professores"].append(novo_professor)
    db.Database.save_data(data)
    return jsonify(novo_professor), 201

@app.route("/professores/<string:id>", methods=["PUT"])
def update_professor(id):
    data = db.Database.load_data()
    request_data = request.json

    for professor in data["professores"]:
        if professor["id"] == id:
            professor.update(request_data)
            db.Database.save_data(data)
            return jsonify(professor)

    return jsonify({"erro": "Professor não encontrado"}), 404

@app.route("/professores/<string:id>", methods=["DELETE"])
def delete_professor(id):
    data = db.Database.load_data()
    data["professores"] = [p for p in data["professores"] if p["id"] != id]
    db.Database.save_data(data)
    return jsonify({"mensagem": "Professor removido com sucesso"})

@app.route("/turmas", methods=["GET"])
def get_turmas():
    data = db.Database.load_data()
    return jsonify(data["turmas"])

@app.route("/turmas/<string:id>", methods=["GET"])
def get_turma(id):
    data = db.Database.load_data()
    for turma in data["turmas"]:
        if turma["id"] == id:
            return jsonify(turma)
    return jsonify({"erro": "Turma não encontrado"}), 404

@app.route("/turmas", methods=["POST"])
def post_turma():
    data = db.Database.load_data()
    nova_turma = request.json

    if not validar_nome(nova_turma.get("nome")):
        return jsonify({"erro": "Nome da turma inválido. Não use caracteres especiais."}), 400
    if not isinstance(nova_turma.get("turno"), str) or not nova_turma["turno"].strip():
        return jsonify({"erro": "Turno inválido. Deve ser uma string não vazia."}), 400
    if not isinstance(nova_turma.get("capacidade"), int) or nova_turma["capacidade"] <= 0:
        return jsonify({"erro": "Capacidade inválida. Deve ser um número inteiro positivo."}), 400

    nova_turma["id"] = db.Database.gerar_uuid()
    data["turmas"].append(nova_turma)
    db.Database.save_data(data)
    return jsonify(nova_turma), 201

@app.route("/turmas/<string:id>", methods=["PUT"])
def update_turma(id):
    data = db.Database.load_data()
    request_data = request.json

    for turma in data["turmas"]:
        if turma["id"] == id:
            turma.update(request_data)
            db.Database.save_data(data)
            return jsonify(turma)
    return jsonify({"erro": "Turma não encontrada"}), 404

@app.route("/turmas/<string:id>", methods=["DELETE"])
def delete_turma(id):
    data = db.Database.load_data()
    data["turmas"] = [t for t in data["turmas"] if t["id"] != id]
    db.Database.save_data(data)
    return jsonify({"mensagem": "Turma removida com sucesso"})

@app.route("/alunos", methods=["GET"])
def get_alunos():
    data = db.Database.load_data()
    return jsonify(data["alunos"])

@app.route("/alunos/<string:id>", methods=["GET"])
def get_aluno(id):
    data = db.Database.load_data()
    for aluno in data["alunos"]:
        if aluno["id"] == id:
            return jsonify(aluno)
    return jsonify({"erro": "Aluno não encontrado"}), 404

@app.route("/alunos", methods=["POST"])
def post_aluno():
    data = db.Database.load_data()
    novo_aluno = request.json

    if not validar_nome(novo_aluno.get("nome")):
        return jsonify({"erro": "Nome inválido. Não use caracteres especiais."}), 400
    if not validar_data(novo_aluno.get("data_nascimento")):
        return jsonify({"erro": "Data de nascimento inválida. Use o formato YYYY-MM-DD."}), 400

    try:
        novo_aluno["nota_primeiro_semestre"] = float(novo_aluno["nota_primeiro_semestre"])
        novo_aluno["nota_segundo_semestre"] = float(novo_aluno["nota_segundo_semestre"])
    except ValueError:
        return jsonify({"erro": "As notas devem ser valores numéricos."}), 400

    novo_aluno["id"] = db.Database.gerar_uuid()
    data["alunos"].append(novo_aluno)
    db.Database.save_data(data)

    return jsonify(novo_aluno), 201

@app.route("/alunos/<string:id>", methods=["PUT"])
def update_aluno(id):
    data = db.Database.load_data()
    request_data = request.json

    for aluno in data["alunos"]:
        if aluno["id"] == id:
            aluno.update(request_data)
            db.Database.save_data(data)
            return jsonify(aluno)
    return jsonify({"erro": "Aluno não encontrado"}), 404

@app.route("/alunos/<string:id>", methods=["DELETE"])
def delete_aluno(id):
    data = db.Database.load_data()
    data["alunos"] = [a for a in data["alunos"] if a["id"] != id]
    db.Database.save_data(data)
    return jsonify({"mensagem": "Aluno removido com sucesso"})

@app.route("/delete_all", methods=["DELETE"])
def delete_all():
    data = db.Database.load_data()
    data["professores"] = []
    data["turmas"] = []
    data["alunos"] = []
    db.Database.save_data(data)
    return jsonify({"mensagem": "Todos os dados foram removidos"})

if __name__ == '__main__':
    app.run(debug=True)
