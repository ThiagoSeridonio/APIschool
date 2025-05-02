from flask import Blueprint, request, jsonify
from model.professores_models import Professor
from model.turmas_models import Turma
from config import db
import re

prof_rotas = Blueprint('professores', __name__)

@prof_rotas.route('/professores', methods=['GET'], strict_slashes=False)
def listar_professores():
    professores = Professor.query.all()
    return jsonify([p.to_dict() for p in professores])

@prof_rotas.route('/professores/<int:id>', methods=['GET'], strict_slashes=False)
def obter_professor(id):
    professor = Professor.query.get(id)
    if professor:
        return jsonify(professor.to_dict())
    return jsonify({'erro': 'Professor não encontrado'}), 404

@prof_rotas.route('/professores', methods=['POST'], strict_slashes=False)
def criar_professor():
    dados = request.get_json()
    print(dados)
    
    if 'email' not in dados:
        return {'erro': 'Email é obrigatório'}, 400
    
    existing_professor = Professor.query.filter_by(email=dados['email']).first()
    if existing_professor:
        return jsonify({'erro': 'Email já cadastrado'}), 400
    
    if not dados.get('nome'):
        return jsonify({'erro': 'Nome é obrigatório'}), 400
    
    if not dados.get('data_nascimento'):
        return jsonify({'erro': 'Data de nascimento é obrigatória'}), 400
    
    if not re.match(r"^[A-Za-zÀ-ÿ\s\.\-]+$", dados.get('nome', '')):
        return jsonify({'erro': 'Nome contém caracteres inválidos'}), 400

    try:
        novo_professor = Professor(
            nome=dados['nome'],
            data_nascimento=dados['data_nascimento'],
            disciplina=dados.get('disciplina', ''),
            salario=dados.get('salario', None),
            email=dados['email']
        )
        db.session.add(novo_professor)
        db.session.commit()
        return jsonify(novo_professor.to_dict()), 201
    except Exception as e:
        print(f"Erro: {e}") 
        return jsonify({'erro': str(e)}), 400


@prof_rotas.route('/professores/<int:id>', methods=['PUT'], strict_slashes=False)
def atualizar_professor(id):
    professor = Professor.query.get(id)
    if not professor:
        return jsonify({'erro': 'Professor não encontrado'}), 404

    dados = request.get_json()
    for chave, valor in dados.items():
        setattr(professor, chave, valor)
    db.session.commit()
    return jsonify(professor.to_dict())

@prof_rotas.route('/professores/<int:id>', methods=['DELETE'], strict_slashes=False)
def deletar_professor(id):
    professor = Professor.query.get_or_404(id)

    turmas_vinculadas = Turma.query.filter_by(professor_id=id).all()
    if turmas_vinculadas:
        return jsonify({"erro": "Não é possível deletar o professor. Ele está vinculado a uma ou mais turmas."}), 400

    db.session.delete(professor)
    db.session.commit()
    return jsonify({"mensagem": "Professor deletado com sucesso"}), 200
