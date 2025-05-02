from flask import Blueprint, request, jsonify
from model.alunos_models import Aluno
from config import db
import re

alunos_rotas = Blueprint('alunos', __name__)

@alunos_rotas.route('/alunos', methods=['GET'], strict_slashes=False)
def listar_alunos():
    alunos = Aluno.query.all()
    return jsonify([aluno.to_dict() for aluno in alunos]), 200

@alunos_rotas.route('/alunos/<int:id>', methods=['GET'], strict_slashes=False)
def buscar_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    return jsonify(aluno.to_dict()), 200

@alunos_rotas.route('/alunos', methods=['POST'], strict_slashes=False)
def criar_aluno():
    dados = request.get_json()

    if 'nome' not in dados or not dados['nome']:
        return jsonify({'erro': 'Nome é obrigatório'}), 400

    if not isinstance(dados['nome'], str) or not re.match(r'^[A-Za-zÀ-ÿ\s]+$', dados['nome']):
        return jsonify({'erro': 'Nome inválido. Apenas letras e espaços são permitidos.'}), 400

    if 'data_nascimento' not in dados or not dados['data_nascimento']:
        return jsonify({'erro': 'Data de nascimento é obrigatória'}), 400

    try:
        novo_aluno = Aluno(
            nome=dados['nome'],
            data_nascimento=dados['data_nascimento'],
            nota1=dados.get('nota1', 0.0),
            nota2=dados.get('nota2', 0.0)
        )
        db.session.add(novo_aluno)
        db.session.commit()
        return jsonify(novo_aluno.to_dict()), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400


@alunos_rotas.route('/alunos/<int:id>', methods=['PUT'], strict_slashes=False)
def atualizar_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    dados = request.get_json()
    aluno.nome = dados.get('nome', aluno.nome)
    aluno.data_nascimento = dados.get('data_nascimento', aluno.data_nascimento)
    aluno.notas = dados.get('notas', aluno.notas)
    db.session.commit()
    return jsonify(aluno.to_dict()), 200

@alunos_rotas.route('/alunos/<int:id>', methods=['DELETE'], strict_slashes=False)
def deletar_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    return jsonify({'mensagem': 'Aluno deletado com sucesso.'}), 200
