from config import db, app
from model.professores_models import Professor
from model.alunos_models import Aluno
from model.turmas_models import Turma

with app.app_context():
    db.drop_all()
    db.create_all()

    # Criar professores
    prof1 = Professor(nome="Carlos Silva", data_nascimento="1980-06-10", disciplina="Matemática", email="carlos.silva@email.com", salario=5000.99)
    prof2 = Professor(nome="Ana Costa", data_nascimento="1975-09-20", disciplina="História", email="ana.costa@email.com", salario=5000.99)

    db.session.add_all([prof1, prof2])
    db.session.commit()

    # Criar alunos
    aluno1 = Aluno(nome="João Oliveira", data_nascimento="2005-03-15", nota1=8.0, nota2=7.5)
    aluno2 = Aluno(nome="Maria Souza", data_nascimento="2004-11-02", nota1=9.0, nota2=8.5)
    aluno3 = Aluno(nome="Lucas Lima", data_nascimento="2005-07-22", nota1=6.0, nota2=7.0)

    db.session.add_all([aluno1, aluno2, aluno3])
    db.session.commit()

    # Criar turma com professor e alunos
    turma1 = Turma(nome="Turma A", professor_id=prof1.id)
    turma1.alunos.extend([aluno1, aluno2])

    turma2 = Turma(nome="Turma B", professor_id=prof2.id)
    turma2.alunos.append(aluno3)

    db.session.add_all([turma1, turma2])
    db.session.commit()

    print("Banco de dados populado com sucesso!")
