from flask import Blueprint, jsonify, request
from . import professores_models as model

prof_rotas = Blueprint("prof_rotas", __name__)

@prof_rotas.route("/professores", methods=["GET"])
def get_professores():
    return jsonify(model.listar_professores())

@prof_rotas.route("/professores/<string:id>", methods=["GET"])
def get_professor(id):
    professor = model.buscar_professor_por_id(id)
    if professor:
        return jsonify(professor)
    return jsonify({"erro": "Professor não encontrado"}), 404

@prof_rotas.route("/professores", methods=["POST"])
def post_professor():
    novo = request.json

    if not model.validar_nome(novo.get("nome")):
        return jsonify({"erro": "Nome inválido. Não use caracteres especiais."}), 400
    if not model.validar_data(novo.get("data_nascimento")):
        return jsonify({"erro": "Data de nascimento inválida. Use o formato YYYY-MM-DD."}), 400
    if not isinstance(novo.get("disciplina"), str) or not novo["disciplina"].strip():
        return jsonify({"erro": "Disciplina inválida. Deve ser uma string não vazia."}), 400
    if not isinstance(novo.get("salario"), (float, int)):
        return jsonify({"erro": "Salário inválido. Deve ser um número."}), 400

    professor = model.adicionar_professor(novo)
    return jsonify(professor), 201

@prof_rotas.route("/professores/<string:id>", methods=["PUT"])
def update_professor(id):
    dados = request.json

    if "nome" in dados and not model.validar_nome(dados["nome"]):
        return jsonify({"erro": "Nome inválido."}), 400
    if "data_nascimento" in dados and not model.validar_data(dados["data_nascimento"]):
        return jsonify({"erro": "Data inválida."}), 400
    if "disciplina" in dados and (not isinstance(dados["disciplina"], str) or not dados["disciplina"].strip()):
        return jsonify({"erro": "Disciplina inválida."}), 400
    if "salario" in dados and not isinstance(dados["salario"], (float, int)):
        return jsonify({"erro": "Salário inválido."}), 400

    professor = model.atualizar_professor(id, dados)
    if professor:
        return jsonify(professor)
    return jsonify({"erro": "Professor não encontrado"}), 404

@prof_rotas.route("/professores/<string:id>", methods=["DELETE"])
def delete_professor(id):
    if model.remover_professor(id):
        return jsonify({"mensagem": "Professor removido com sucesso"})
    return jsonify({"erro": "Professor não encontrado"}), 404
