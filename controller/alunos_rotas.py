from flask import Blueprint, jsonify, request
from model import alunos_models as model
from model.alunos_models import ErroValidacao, ErroAlunoNaoEncontrado

alunos_rotas = Blueprint("alunos_rotas", __name__)

@alunos_rotas.route("/alunos", methods=["GET"])
def get_alunos():
    return jsonify(model.listar_alunos())

@alunos_rotas.route("/alunos/<string:id>", methods=["GET"])
def get_aluno(id):
    try:
        aluno = model.buscar_aluno_por_id(id)
        return jsonify(aluno)
    except ErroAlunoNaoEncontrado as e:
        return jsonify({"erro": str(e)}), e.status

@alunos_rotas.route("/alunos", methods=["POST"])
def post_aluno():
    novo_aluno = request.json
    try:
        model.validar_aluno(novo_aluno)
        aluno = model.adicionar_aluno(novo_aluno)
        return jsonify(aluno), 201
    except ErroValidacao as e:
        return jsonify({"erro": str(e)}), e.status

@alunos_rotas.route("/alunos/<string:id>", methods=["PUT"])
def update_aluno(id):
    dados = request.json

    try:
        if "nome" in dados and not model.validar_nome(dados["nome"]):
            raise model.NomeInvalidoErro("Nome inválido.")
        if "data_nascimento" in dados and not model.validar_data(dados["data_nascimento"]):
            raise model.DataInvalidaErro("Data inválida.")

        if "nota_primeiro_semestre" in dados:
            dados["nota_primeiro_semestre"] = float(dados["nota_primeiro_semestre"])
        if "nota_segundo_semestre" in dados:
            dados["nota_segundo_semestre"] = float(dados["nota_segundo_semestre"])

        aluno = model.atualizar_aluno(id, dados)
        return jsonify(aluno)

    except ValueError:
        return jsonify({"erro": "Notas devem ser numéricas."}), 400
    except ErroValidacao as e:
        return jsonify({"erro": str(e)}), e.status

@alunos_rotas.route("/alunos/<string:id>", methods=["DELETE"])
def delete_aluno(id):
    try:
        model.remover_aluno(id)
        return jsonify({"mensagem": "Aluno removido com sucesso"})
    except ErroAlunoNaoEncontrado as e:
        return jsonify({"erro": str(e)}), e.status
