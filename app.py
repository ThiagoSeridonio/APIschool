from flask import Flask, jsonify, request
import database as db

app = Flask(__name__)


## Professores
@app.route("/professores", methods=["GET"])
def get_professores():
    data = db.Database.load_data()
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
    novo_professor["id"] = db.Database.gerar_uuid()
    data["professores"].append(novo_professor)
    db.Database.save_data(data)
    return jsonify(novo_professor), 201


@app.route("/professores/<string:id>", methods=["PUT"])
def update_professor(id):
    data = db.Database.load_data()
    for professor in data["professores"]:
        if professor["id"] == id:
            professor.update(request.json)
            db.Database.save_data(data)
            return jsonify(professor)
    return jsonify({"erro": "Professor não encontrado"}), 404


@app.route("/professores/<string:id>", methods=["DELETE"])
def delete_professor(id):
    data = db.Database.load_data()
    data["professores"] = [p for p in data["professores"] if p["id"] != id]
    db.Database.save_data(data)
    return jsonify({"mensagem": "Professor removido com sucesso"})


##Turmas
@app.route("/turmas", methods=["GET"])
def get_turmas():
    data = db.Database.load_data()
    return jsonify(data["turmas"])


@app.route("/turmas", methods=["POST"])
def post_turma():
    data = db.Database.load_data()
    nova_turma = request.json
    nova_turma["id"] = db.Database.gerar_uuid()
    data["turmas"].append(nova_turma)
    db.Database.save_data(data)
    return jsonify(nova_turma), 201


@app.route("/turmas/<string:id>", methods=["PUT"])
def update_turma(id):
    data = db.Database.load_data()
    for turma in data["turmas"]:
        if turma["id"] == id:
            turma.update(request.json)
            db.Database.save_data(data)
            return jsonify(turma)
    return jsonify({"erro": "Turma não encontrada"}), 404


@app.route("/turmas/<string:id>", methods=["DELETE"])
def delete_turma(id):
    data = db.Database.load_data()
    data["turmas"] = [t for t in data["turmas"] if t["id"] != id]
    db.Database.save_data(data)
    return jsonify({"mensagem": "Turma removida com sucesso"})


## Alunos
@app.route("/alunos", methods=["GET"])
def get_alunos():
    data = db.Database.load_data()
    return jsonify(data["alunos"])


@app.route("/alunos", methods=["POST"])
def post_aluno():
    data = db.Database.load_data()
    novo_aluno = request.json
    novo_aluno["id"] = db.Database.gerar_uuid()
    data["alunos"].append(novo_aluno)
    db.Database.save_data(data)
    return jsonify(novo_aluno), 201


@app.route("/alunos/<string:id>", methods=["PUT"])
def update_aluno(id):
    data = db.Database.load_data()
    for aluno in data["alunos"]:
        if aluno["id"] == id:
            aluno.update(request.json)
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
