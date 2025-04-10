import re
import datetime
import database as db


# ====================
# Exceções personalizadas
# ====================

class ErroValidacao(Exception):
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

class DisciplinaInvalidaErro(ErroValidacao):
    def __init__(self):
        super().__init__("Disciplina inválida. Deve ser uma string não vazia.")

class SalarioInvalidoErro(ErroValidacao):
    def __init__(self):
        super().__init__("Salário inválido. Deve ser um número.")

class ErroProfessorNaoEncontrado(ErroValidacao):
    def __init__(self):
        super().__init__("Professor não encontrado", status=404)


# ====================
# Validações
# ====================

def validar_nome(nome):
    return isinstance(nome, str) and re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s]+$", nome)

def validar_data(data):
    return isinstance(data, str) and re.match(r"^\d{4}-\d{2}-\d{2}$", data)

def calcular_idade(data_nascimento):
    if not validar_data(data_nascimento):
        return None
    ano_nascimento = int(data_nascimento.split("-")[0])
    return datetime.datetime.now().year - ano_nascimento


# ====================
# Operações com dados
# ====================

def validar_professor(dados):
    campos_obrigatorios = ["nome", "data_nascimento", "disciplina", "salario"]
    for campo in campos_obrigatorios:
        if campo not in dados:
            raise CampoObrigatorioErro(campo)

    if not validar_nome(dados["nome"]):
        raise NomeInvalidoErro()
    if not validar_data(dados["data_nascimento"]):
        raise DataInvalidaErro()
    if not isinstance(dados["disciplina"], str) or not dados["disciplina"].strip():
        raise DisciplinaInvalidaErro()
    if not isinstance(dados["salario"], (int, float)):
        raise SalarioInvalidoErro()


def listar_professores():
    data = db.Database.load_data()
    for professor in data["professores"]:
        professor["idade"] = calcular_idade(professor.get("data_nascimento", ""))
    return data["professores"]

def buscar_professor_por_id(prof_id):
    data = db.Database.load_data()
    for professor in data["professores"]:
        if professor["id"] == prof_id:
            return professor
    return None

def adicionar_professor(novo_professor):
    validar_professor(novo_professor)

    data = db.Database.load_data()
    novo_professor["id"] = db.Database.gerar_uuid()
    data["professores"].append(novo_professor)
    db.Database.save_data(data)
    return novo_professor

def atualizar_professor(prof_id, novos_dados):
    data = db.Database.load_data()

    for professor in data["professores"]:
        if professor["id"] == prof_id:
            # validações parciais
            if "nome" in novos_dados and not validar_nome(novos_dados["nome"]):
                raise NomeInvalidoErro()
            if "data_nascimento" in novos_dados and not validar_data(novos_dados["data_nascimento"]):
                raise DataInvalidaErro()
            if "disciplina" in novos_dados and (not isinstance(novos_dados["disciplina"], str) or not novos_dados["disciplina"].strip()):
                raise DisciplinaInvalidaErro()
            if "salario" in novos_dados and not isinstance(novos_dados["salario"], (int, float)):
                raise SalarioInvalidoErro()

            professor.update(novos_dados)
            db.Database.save_data(data)
            return professor

    raise ErroProfessorNaoEncontrado()

def remover_professor(prof_id):
    data = db.Database.load_data()
    professores = data["professores"]
    nova_lista = [p for p in professores if p["id"] != prof_id]
    if len(nova_lista) == len(professores):
        raise ErroProfessorNaoEncontrado()

    data["professores"] = nova_lista
    db.Database.save_data(data)
    return True
