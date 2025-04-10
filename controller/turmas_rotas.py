from flask import Blueprint, jsonify, request
from model import turmas_models as model
from model.turmas_models import ErroValidacao, ErroTurmaNaoEncontrada

turmas_rotas = Blueprint("turmas_rotas", __name__)

@turmas_rotas.route("/turmas", methods=["GET"])
def get_turmas():
    return jsonify(model.listar_turmas())

@turmas_rotas.route("/turmas/<string:id>", methods=["GET"])
def get_turma(id):
    try:
        turma = model.buscar_turma_por_id(id)
        return jsonify(turma)
    except ErroValidacao as e:
        return jsonify({"erro": str(e)}), e.status

@turmas_rotas.route("/turmas", methods=["POST"])
def post_turma():
    try:
        nova_turma = request.json
        turma = model.adicionar_turma(nova_turma)
        return jsonify(turma), 201
    except ErroValidacao as e:
        return jsonify({"erro": str(e)}), e.status

@turmas_rotas.route("/turmas/<string:id>", methods=["PUT"])
def update_turma(id):
    try:
        dados = request.json
        turma = model.atualizar_turma(id, dados)
        return jsonify(turma)
    except ErroValidacao as e:
        return jsonify({"erro": str(e)}), e.status

@turmas_rotas.route("/turmas/<string:id>", methods=["DELETE"])
def delete_turma(id):
    try:
        model.remover_turma(id)
        return jsonify({"mensagem": "Turma removida com sucesso"})
    except ErroValidacao as e:
        return jsonify({"erro": str(e)}), e.status
