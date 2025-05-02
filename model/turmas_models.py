import re
from config import db
from model.alunos_models import Aluno
from model.professores_models import Professor

class Turma(db.Model):
    __tablename__ = 'turmas'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'), nullable=False)

    professor = db.relationship('Professor', backref=db.backref('turmas', lazy=True))
    alunos = db.relationship('Aluno', secondary='alunos_turmas', backref='turmas')

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "professor_id": self.professor_id,
            "professor_nome": self.professor.nome if self.professor else None,
            "alunos": [aluno.id for aluno in self.alunos]
        }

# Tabela intermediária aluno <-> turma
alunos_turmas = db.Table('alunos_turmas',
    db.Column('aluno_id', db.Integer, db.ForeignKey('alunos.id'), primary_key=True),
    db.Column('turma_id', db.Integer, db.ForeignKey('turmas.id'), primary_key=True)
)


# Exceções personalizadas
class ErroValidacao(Exception):
    def __init__(self, mensagem, status=400):
        self.mensagem = mensagem
        self.status = status
        super().__init__(mensagem)

    def __str__(self):
        return self.mensagem

class ErroTurmaNaoEncontrada(ErroValidacao):
    def __init__(self):
        super().__init__("Turma não encontrada", 404)

# Validações
def validar_nome(nome):
    return isinstance(nome, str) and re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", nome)

def validar_turma(turma):
    if not validar_nome(turma.get("nome", "")):
        raise ErroValidacao("Nome da turma inválido. Não use caracteres especiais.")
    if not isinstance(turma.get("turno"), str) or not turma["turno"].strip():
        raise ErroValidacao("Turno inválido. Deve ser uma string não vazia.")
    if not isinstance(turma.get("capacidade"), int) or turma["capacidade"] <= 0:
        raise ErroValidacao("Capacidade inválida. Deve ser um número inteiro positivo.")

# Operações
def listar_turmas():
    return db.Database.load_data()["turmas"]

def buscar_turma_por_id(id):
    turma = next((t for t in listar_turmas() if t["id"] == id), None)
    if not turma:
        raise ErroTurmaNaoEncontrada()
    return turma

def adicionar_turma(turma):
    validar_turma(turma)
    data = db.Database.load_data()
    turma["id"] = db.Database.gerar_uuid()
    data["turmas"].append(turma)
    db.Database.save_data(data)
    return turma

def atualizar_turma(id, dados):
    data = db.Database.load_data()
    turma_encontrada = None
    for turma in data["turmas"]:
        if turma["id"] == id:
            turma_encontrada = turma
            break
    if not turma_encontrada:
        raise ErroTurmaNaoEncontrada()

    if "nome" in dados and not validar_nome(dados["nome"]):
        raise ErroValidacao("Nome da turma inválido.")

    turma_encontrada.update(dados)
    db.Database.save_data(data)
    return turma_encontrada

def remover_turma(id):
    data = db.Database.load_data()
    turmas = data["turmas"]
    nova_lista = [t for t in turmas if t["id"] != id]
    if len(nova_lista) == len(turmas):
        raise ErroTurmaNaoEncontrada()
    data["turmas"] = nova_lista
    db.Database.save_data(data)
    return True