from flask import Blueprint, jsonify, request
from . import alunos_models as model

alunos_rotas = Blueprint("alunos_rotas", __name__)

@alunos_rotas.route("/alunos", methods=["GET"])
def get_alunos():
    return jsonify(model.listar_alunos())

@alunos_rotas.route("/alunos/<string:id>", methods=["GET"])
def get_aluno(id):
    aluno = model.buscar_aluno_por_id(id)
    if aluno:
        return jsonify(aluno)
    return jsonify({"erro": "Aluno não encontrado"}), 404

@alunos_rotas.route("/alunos", methods=["POST"])
def post_aluno():
    novo_aluno = request.json
    erro = model.validar_aluno(novo_aluno)
    if erro:
        return jsonify({"erro": erro[0]}), erro[1]

    aluno = model.adicionar_aluno(novo_aluno)
    return jsonify(aluno), 201

@alunos_rotas.route("/alunos/<string:id>", methods=["PUT"])
def update_aluno(id):
    dados = request.json

    # validações parciais, se quiser
    if "nome" in dados and not model.validar_nome(dados["nome"]):
        return jsonify({"erro": "Nome inválido."}), 400
    if "data_nascimento" in dados and not model.validar_data(dados["data_nascimento"]):
        return jsonify({"erro": "Data inválida."}), 400

    try:
        if "nota_primeiro_semestre" in dados:
            dados["nota_primeiro_semestre"] = float(dados["nota_primeiro_semestre"])
        if "nota_segundo_semestre" in dados:
            dados["nota_segundo_semestre"] = float(dados["nota_segundo_semestre"])
    except ValueError:
        return jsonify({"erro": "Notas devem ser numéricas."}), 400

    aluno = model.atualizar_aluno(id, dados)
    if aluno:
        return jsonify(aluno)
    return jsonify({"erro": "Aluno não encontrado"}), 404

@alunos_rotas.route("/alunos/<string:id>", methods=["DELETE"])
def delete_aluno(id):
    if model.remover_aluno(id):
        return jsonify({"mensagem": "Aluno removido com sucesso"})
    return jsonify({"erro": "Aluno não encontrado"}), 404
