from flask import Blueprint, request, jsonify
from model.turmas_models import Turma, alunos_turmas
from model.alunos_models import Aluno
from model.professores_models import Professor
from config import db


turmas_rotas = Blueprint('turmas', __name__)

@turmas_rotas.route('/turmas', methods=['GET'], strict_slashes=False)
def listar_turmas():
    turmas = Turma.query.all()
    return jsonify([t.to_dict() for t in turmas])

@turmas_rotas.route('/turmas/<int:id>', methods=['GET'], strict_slashes=False)
def obter_turma(id):
    turma = Turma.query.get(id)
    if turma:
        return jsonify(turma.to_dict())
    return jsonify({'erro': 'Turma não encontrada'}), 404

@turmas_rotas.route('/turmas', methods=['POST'], strict_slashes=False)
def criar_turma():
    dados = request.get_json()

    if not dados.get('nome'):
        return jsonify({'erro': 'Nome da turma é obrigatório'}), 400

    if not dados.get('professor_id'):
        return jsonify({'erro': 'ID do professor é obrigatório'}), 400

    professor = Professor.query.get(dados['professor_id'])
    if not professor:
        return jsonify({'erro': 'Professor não encontrado'}), 400

    try:
        nova_turma = Turma(
            nome=dados['nome'],
            professor_id=dados['professor_id']
        )
        db.session.add(nova_turma)
        db.session.commit()
        return jsonify(nova_turma.to_dict()), 201
    except Exception as e:
        return jsonify({'erro': f"Erro inesperado: {str(e)}"}), 400


@turmas_rotas.route('/turmas/<int:id>', methods=['PUT'], strict_slashes=False)
def atualizar_turma(id):
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({'erro': 'Turma não encontrada'}), 404

    dados = request.get_json()
    turma.nome = dados.get('nome', turma.nome)
    
    if 'professor_id' in dados:
        if not Professor.query.get(dados['professor_id']):
            return jsonify({'erro': 'Professor não encontrado'}), 400
        turma.professor_id = dados['professor_id']

    if 'alunos' in dados:
        turma.alunos = []
        for aluno_id in dados['alunos']:
            aluno = Aluno.query.get(aluno_id)
            if aluno:
                turma.alunos.append(aluno)

    db.session.commit()
    return jsonify(turma.to_dict())

@turmas_rotas.route('/turmas/<int:id>', methods=['DELETE'], strict_slashes=False)
def deletar_turma(id):
    turma = Turma.query.get(id)
    if not turma:
        return jsonify({'erro': 'Turma não encontrada'}), 404

    db.session.delete(turma)
    db.session.commit()
    return jsonify({'mensagem': 'Turma removida com sucesso'})
