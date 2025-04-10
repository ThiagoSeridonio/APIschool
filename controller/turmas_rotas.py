from flask import Blueprint, jsonify, request
from model import turmas_models as model

turmas_rotas = Blueprint("turmas_rotas", __name__)

@turmas_rotas.route("/turmas", methods=["GET"])
def get_turmas():
    return jsonify(model.listar_turmas())

@turmas_rotas.route("/turmas/<string:id>", methods=["GET"])
def get_turma(id):
    turma = model.buscar_turma_por_id(id)
    if turma:
        return jsonify(turma)
    return jsonify({"erro": "Turma não encontrada"}), 404

@turmas_rotas.route("/turmas", methods=["POST"])
def post_turma():
    nova_turma = request.json
    erro = model.validar_turma(nova_turma)
    if erro:
        return jsonify({"erro": erro[0]}), erro[1]

    turma = model.adicionar_turma(nova_turma)
    return jsonify(turma), 201

@turmas_rotas.route("/turmas/<string:id>", methods=["PUT"])
def update_turma(id):
    dados = request.json

    if "nome" in dados and not model.validar_nome(dados["nome"]):
        return jsonify({"erro": "Nome da turma inválido."}), 400

    turma = model.atualizar_turma(id, dados)
    if turma:
        return jsonify(turma)
    return jsonify({"erro": "Turma não encontrada"}), 404

@turmas_rotas.route("/turmas/<string:id>", methods=["DELETE"])
def delete_turma(id):
    if model.remover_turma(id):
        return jsonify({"mensagem": "Turma removida com sucesso"})
    return jsonify({"erro": "Turma não encontrada"}), 404
