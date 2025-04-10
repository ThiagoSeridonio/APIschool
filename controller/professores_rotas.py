from flask import Blueprint, jsonify, request
from model import professores_models as model
from model.professores_models import ErroValidacao, ErroProfessorNaoEncontrado

prof_rotas = Blueprint("prof_rotas", __name__)

@prof_rotas.route("/professores", methods=["GET"])
def get_professores():
    return jsonify(model.listar_professores())

@prof_rotas.route("/professores/<string:id>", methods=["GET"])
def get_professor(id):
    try:
        professor = model.buscar_professor_por_id(id)
        if not professor:
            raise ErroProfessorNaoEncontrado()
        return jsonify(professor)
    except ErroValidacao as e:
        return jsonify({"erro": str(e)}), e.status

@prof_rotas.route("/professores", methods=["POST"])
def post_professor():
    try:
        novo = request.json
        professor = model.adicionar_professor(novo)
        return jsonify(professor), 201
    except ErroValidacao as e:
        return jsonify({"erro": str(e)}), e.status

@prof_rotas.route("/professores/<string:id>", methods=["PUT"])
def update_professor(id):
    try:
        dados = request.json
        professor = model.atualizar_professor(id, dados)
        return jsonify(professor)
    except ErroValidacao as e:
        return jsonify({"erro": str(e)}), e.status

@prof_rotas.route("/professores/<string:id>", methods=["DELETE"])
def delete_professor(id):
    try:
        model.remover_professor(id)
        return jsonify({"mensagem": "Professor removido com sucesso"})
    except ErroValidacao as e:
        return jsonify({"erro": str(e)}), e.status
