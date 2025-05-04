from flask_restx import Namespace, Resource, fields
from flask import request
from model.turmas_models import Turma, ErroTurmaNaoEncontrada, ErroValidacao, db
from model.professores_models import Professor
from model.alunos_models import Aluno

api = Namespace('Turmas', description='Operações com turmas')

# Modelo de entrada/saída para a API (Swagger)
turma_model = api.model('Turma', {
    'id': fields.Integer(readOnly=True, description='ID da turma'),
    'nome': fields.String(required=True, description='Nome da turma'),
    'professor_id': fields.Integer(required=True, description='ID do professor responsável'),
    'professor_nome': fields.String(readOnly=True, description='Nome do professor'),
    'alunos': fields.List(fields.Integer, description='Lista de IDs dos alunos')
})

@api.route('/')
class TurmaList(Resource):
    @api.marshal_list_with(turma_model)
    def get(self):
        """Lista todas as turmas"""
        turmas = Turma.query.all()
        return [t.to_dict() for t in turmas]

    @api.expect(turma_model)
    @api.marshal_with(turma_model, code=201)
    def post(self):
        """Cria uma nova turma"""
        dados = request.json

        if not isinstance(dados.get("nome"), str) or not dados["nome"].strip():
            raise ErroValidacao("Nome da turma inválido.")
        if not isinstance(dados.get("professor_id"), int):
            raise ErroValidacao("ID do professor inválido.")

        professor = Professor.query.get(dados["professor_id"])
        if not professor:
            raise ErroValidacao("Professor não encontrado.")

        nova_turma = Turma(nome=dados["nome"], professor_id=dados["professor_id"])

        # Associar alunos (opcional)
        if "alunos" in dados:
            alunos_ids = dados["alunos"]
            alunos = Aluno.query.filter(Aluno.id.in_(alunos_ids)).all()
            nova_turma.alunos = alunos

        db.session.add(nova_turma)
        db.session.commit()
        return nova_turma.to_dict(), 201

@api.route('/<int:id>')
@api.param('id', 'ID da turma')
class TurmaResource(Resource):
    @api.marshal_with(turma_model)
    def get(self, id):
        """Busca uma turma por ID"""
        turma = Turma.query.get(id)
        if not turma:
            raise ErroTurmaNaoEncontrada()
        return turma.to_dict()

    @api.expect(turma_model)
    @api.marshal_with(turma_model)
    def put(self, id):
        """Atualiza uma turma"""
        turma = Turma.query.get(id)
        if not turma:
            raise ErroTurmaNaoEncontrada()

        dados = request.json
        if "nome" in dados:
            if not isinstance(dados["nome"], str) or not dados["nome"].strip():
                raise ErroValidacao("Nome da turma inválido.")
            turma.nome = dados["nome"]

        if "professor_id" in dados:
            professor = Professor.query.get(dados["professor_id"])
            if not professor:
                raise ErroValidacao("Professor não encontrado.")
            turma.professor_id = dados["professor_id"]

        if "alunos" in dados:
            alunos_ids = dados["alunos"]
            alunos = Aluno.query.filter(Aluno.id.in_(alunos_ids)).all()
            turma.alunos = alunos

        db.session.commit()
        return turma.to_dict()

    def delete(self, id):
        """Remove uma turma"""
        turma = Turma.query.get(id)
        if not turma:
            raise ErroTurmaNaoEncontrada()
        db.session.delete(turma)
        db.session.commit()
        return {"message": "Turma removida com sucesso"}, 200
