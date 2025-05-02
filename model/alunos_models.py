import re
from datetime import datetime
from config import db

class Aluno(db.Model):
    __tablename__ = 'alunos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.String(10), nullable=False)
    nota1 = db.Column(db.Float, nullable=True)
    nota2 = db.Column(db.Float, nullable=True)
    
    def calcular_media(self):
        if not self.nota1 or not self.nota2:
            return 0
        return (self.nota1 + self.nota2) / 2 

    def calcular_idade(self):
        try:
            nascimento = datetime.strptime(self.data_nascimento, "%Y-%m-%d")
        except ValueError:
            nascimento = datetime.strptime(self.data_nascimento, "%d/%m/%Y")
        idade = (datetime.now() - nascimento).days // 365
        return idade

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "data_nascimento": self.data_nascimento,
            "nota1": self.nota1,
            "nota2": self.nota2,
            "media": self.calcular_media(),
            "idade": self.calcular_idade()
        }
        
        
# Exceções personalizadas

class ErroValidacao(Exception):
    """Erro genérico de validação."""
    def __init__(self, mensagem, status=400):
        super().__init__(mensagem)
        self.status = status

class CampoObrigatorioErro(ErroValidacao):
    def __init__(self, campo):
        super().__init__(f"O campo '{campo}' é obrigatório.")

class NomeInvalidoErro(ErroValidacao):
    def __init__(self):
        super().__init__("O nome deve ser uma string válida sem caracteres especiais.")

class DataInvalidaErro(ErroValidacao):
    def __init__(self):
        super().__init__("A data de nascimento deve estar no formato YYYY-MM-DD.")

class NotaInvalidaErro(ErroValidacao):
    def __init__(self):
        super().__init__("As notas devem ser valores numéricos.")

class ErroAlunoNaoEncontrado(ErroValidacao):
    def __init__(self):
        super().__init__("Aluno não encontrado", status=404)


# Funções de validação e manipulação de dados

def validar_nome(nome):
    return isinstance(nome, str) and re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", nome)

def validar_data(data):
    return isinstance(data, str) and re.match(r"^\d{4}-\d{2}-\d{2}$", data)

def calcular_idade(data_nascimento):
    if not validar_data(data_nascimento):
        return None
    ano_nascimento = int(data_nascimento.split("-")[0])
    return datetime.datetime.now().year - ano_nascimento

def calcular_media(self):
    return round((self.nota1 + self.nota2) / 2, 2)

def validar_aluno(novo_aluno):
    campos = ["nome", "data_nascimento", "nota_primeiro_semestre", "nota_segundo_semestre"]

    for campo in campos:
        if campo not in novo_aluno:
            raise CampoObrigatorioErro(f"O campo '{campo}' é obrigatório.")

    if not validar_nome(novo_aluno["nome"]):
        raise NomeInvalidoErro("O nome deve ser uma string válida sem caracteres especiais.")

    if not validar_data(novo_aluno["data_nascimento"]):
        raise DataInvalidaErro("A data de nascimento deve estar no formato YYYY-MM-DD.")

    try:
        novo_aluno["nota_primeiro_semestre"] = float(novo_aluno["nota_primeiro_semestre"])
        novo_aluno["nota_segundo_semestre"] = float(novo_aluno["nota_segundo_semestre"])
    except ValueError:
        raise NotaInvalidaErro("As notas devem ser valores numéricos.")

def listar_alunos():
    return db.Database.load_data()["alunos"]

def buscar_aluno_por_id(id):
    alunos = listar_alunos()
    aluno = next((a for a in alunos if a["id"] == id), None)
    if aluno is None:
        raise ErroAlunoNaoEncontrado()
    return aluno

def adicionar_aluno(aluno):
    data = db.Database.load_data()
    aluno["id"] = db.Database.gerar_uuid()
    data["alunos"].append(aluno)
    db.Database.save_data(data)
    return aluno

def atualizar_aluno(id, dados):
    data = db.Database.load_data()
    for aluno in data["alunos"]:
        if aluno["id"] == id:
            aluno.update(dados)
            db.Database.save_data(data)
            return aluno
    raise ErroAlunoNaoEncontrado()

def remover_aluno(id):
    data = db.Database.load_data()
    alunos = data["alunos"]
    nova_lista = [a for a in alunos if a["id"] != id]
    if len(nova_lista) == len(alunos):
        raise ErroAlunoNaoEncontrado()
    data["alunos"] = nova_lista
    db.Database.save_data(data)
    return True