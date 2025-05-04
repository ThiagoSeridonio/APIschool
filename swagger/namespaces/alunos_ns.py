from flask_restx import Namespace, Resource, fields
from flask import request
from model.alunos_models import Aluno, validar_aluno, ErroAlunoNaoEncontrado, db

api = Namespace('Alunos', description='Operações com alunos')

# Modelo para serialização no Swagger
aluno_model = api.model('Aluno', {
    'id': fields.Integer(readOnly=True, description='ID do aluno'),
    'nome': fields.String(required=True, description='Nome do aluno'),
    'data_nascimento': fields.String(required=True, description='Data de nascimento (YYYY-MM-DD)'),
    'nota1': fields.Float(required=False, description='Nota do primeiro semestre'),
    'nota2': fields.Float(required=False, description='Nota do segundo semestre'),
    'media': fields.Float(readOnly=True, description='Média calculada'),
    'idade': fields.Integer(readOnly=True, description='Idade calculada'),
})

@api.route('/')
class AlunoList(Resource):
    @api.marshal_list_with(aluno_model)
    def get(self):
        """Lista todos os alunos"""
        alunos = Aluno.query.all()
        return [aluno.to_dict() for aluno in alunos]

    @api.expect(aluno_model)
    @api.marshal_with(aluno_model, code=201)
    def post(self):
        """Cria um novo aluno"""
        dados = request.json
        validar_aluno({
            "nome": dados.get("nome"),
            "data_nascimento": dados.get("data_nascimento"),
            "nota_primeiro_semestre": dados.get("nota1", 0),
            "nota_segundo_semestre": dados.get("nota2", 0)
        })

        aluno = Aluno(
            nome=dados['nome'],
            data_nascimento=dados['data_nascimento'],
            nota1=dados.get('nota1'),
            nota2=dados.get('nota2')
        )
        db.session.add(aluno)
        db.session.commit()
        return aluno.to_dict(), 201

@api.route('/<int:id>')
@api.param('id', 'ID do aluno')
class AlunoResource(Resource):
    @api.marshal_with(aluno_model)
    def get(self, id):
        """Busca aluno por ID"""
        aluno = Aluno.query.get(id)
        if not aluno:
            raise ErroAlunoNaoEncontrado()
        return aluno.to_dict()

    @api.expect(aluno_model)
    @api.marshal_with(aluno_model)
    def put(self, id):
        """Atualiza um aluno"""
        aluno = Aluno.query.get(id)
        if not aluno:
            raise ErroAlunoNaoEncontrado()

        dados = request.json
        validar_aluno({
            "nome": dados.get("nome"),
            "data_nascimento": dados.get("data_nascimento"),
            "nota_primeiro_semestre": dados.get("nota1", 0),
            "nota_segundo_semestre": dados.get("nota2", 0)
        })

        aluno.nome = dados.get('nome')
        aluno.data_nascimento = dados.get('data_nascimento')
        aluno.nota1 = dados.get('nota1')
        aluno.nota2 = dados.get('nota2')
        db.session.commit()
        return aluno.to_dict()

    def delete(self, id):
        """Remove um aluno"""
        aluno = Aluno.query.get(id)
        if not aluno:
            raise ErroAlunoNaoEncontrado()
        db.session.delete(aluno)
        db.session.commit()
        return {"message": "Aluno removido com sucesso"}, 200
