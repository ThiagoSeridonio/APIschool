from flask_restx import Namespace, Resource, fields
from flask import request
from model.professores_models import Professor, validar_professor, ErroProfessorNaoEncontrado, db

api = Namespace('Professores', description='Operações com professores')

# Modelo para documentação Swagger
professor_model = api.model('Professor', {
    'nome': fields.String(required=True, description='Nome do professor'),
    'email': fields.String(required=True, description='Email do professor'),
    'data_nascimento': fields.String(required=True, description='Data de nascimento (YYYY-MM-DD)'),
    'disciplina': fields.String(required=True, description='Disciplina ministrada'),
    'salario': fields.Float(required=True, description='Salário do professor')
})

@api.route('/')
class ProfessorList(Resource):
    @api.marshal_list_with(professor_model)
    def get(self):
        """Lista todos os professores"""
        professores = Professor.query.all()
        return [p.to_dict() for p in professores]

    @api.expect(professor_model)
    @api.marshal_with(professor_model, code=201)
    def post(self):
        """Cria um novo professor"""
        dados = request.json
        validar_professor(dados)

        professor = Professor(
            nome=dados['nome'],
            email=dados['email'],
            data_nascimento=dados['data_nascimento'],
            disciplina=dados['disciplina'],
            salario=dados['salario']
        )
        db.session.add(professor)
        db.session.commit()
        return professor.to_dict(), 201

@api.route('/<int:id>')
@api.param('id', 'ID do professor')
class ProfessorResource(Resource):
    @api.marshal_with(professor_model)
    def get(self, id):
        """Busca professor por ID"""
        professor = Professor.query.get(id)
        if not professor:
            raise ErroProfessorNaoEncontrado()
        return professor.to_dict()

    @api.expect(professor_model)
    @api.marshal_with(professor_model)
    def put(self, id):
        """Atualiza um professor"""
        professor = Professor.query.get(id)
        if not professor:
            raise ErroProfessorNaoEncontrado()

        dados = request.json
        validar_professor(dados)

        professor.nome = dados['nome']
        professor.email = dados['email']
        professor.data_nascimento = dados['data_nascimento']
        professor.disciplina = dados['disciplina']
        professor.salario = dados['salario']

        db.session.commit()
        return professor.to_dict()

    def delete(self, id):
        """Remove um professor"""
        professor = Professor.query.get(id)
        if not professor:
            raise ErroProfessorNaoEncontrado()
        db.session.delete(professor)
        db.session.commit()
        return {"message": "Professor removido com sucesso"}, 200
