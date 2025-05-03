import unittest
import json
from app import app, db
from unittest.mock import mock_open, patch
from uuid import uuid4


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.app = app.test_client()
        self.client = self.app

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    # Professores

    def test_get_professores(self):
        response = self.app.get("/professores")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_professor_id(self):
        response = self.app.get("/professores/1")
        self.assertTrue(response.status_code in [200, 404])

    def test_post_professor(self):
        novo_professor = {
            "nome": "Carlos Silva",
            "data_nascimento": "1980-05-15",
            "disciplina": "Matemática",
            "salario": 5000.0,
            "email": f"prof_{uuid4()}@email.com"
        }
        response = self.app.post("/professores", json=novo_professor)
        print(response.json)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)
     
    def test_put_professor(self):
        response = self.app.put("/professores/1", json={"salario": 5500.0})
        self.assertTrue(response.status_code in [200, 404])

    def test_delete_professor(self):
        response = self.app.delete("/professores/1")
        self.assertTrue(response.status_code in [200, 404])

    # Turmas
    def test_get_turmas(self):
        response = self.app.get("/turmas")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_turma(self):
        response = self.app.get("/turmas/1")
        self.assertTrue(response.status_code in [200, 404])

    def test_post_turma(self):
        novo_professor = {
        "nome": "Joana Lima",
        "email": "joana@email.com",
        "data_nascimento": "1985-03-22",
        "disciplina": "História",
        "salario": 4800.0
        }
        
        self.client.post('/professores', json=novo_professor)
        
        response_prof = self.client.get('/professores')
        prof_id = response_prof.get_json()[-1]['id']
        
        nova_turma = {
            "nome": "Turma A",
            "turno": "Manhã",
            "capacidade": 30,
            "professor_id": prof_id
        }
        response = self.app.post("/turmas", json=nova_turma)
        self.assertEqual(response.status_code, 201)
        
    def test_put_turma(self):
        response = self.app.put("/turmas/1", json={"capacidade": 35})
        self.assertTrue(response.status_code in [200, 404])

    def test_delete_turma(self):
        response = self.app.delete("/turmas/1")
        self.assertTrue(response.status_code in [200, 404])

    # Alunos
    def test_get_alunos(self):
        response = self.app.get("/alunos")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_aluno(self):
        response = self.app.get("/alunos/1")
        self.assertTrue(response.status_code in [200, 404])

    def test_post_aluno(self):
        novo_aluno = {
            "nome": "Ana Souza",
            "data_nascimento": "2005-09-12",
            "nota1": 8.5,
            "nota2": 9.0
        }
        response = self.app.post("/alunos", json=novo_aluno)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

    def test_put_aluno(self):
        response = self.app.put(
            "/alunos/1", json={"nota_primeiro_semestre": 9.0})
        self.assertTrue(response.status_code in [200, 404])

    def test_delete_aluno(self):
        response = self.app.delete("/alunos/1")
        self.assertTrue(response.status_code in [200, 404])

    # Testes de validação

    def test_nome_e_data_nascimento_professor(self):
        response = self.app.post('/professores', json={
        "nome": "Professor Teste",
        "data_nascimento": "1980-05-10"
    })
        self.assertEqual(response.status_code, 400)
        

    def test_nome_e_data_nascimento_aluno(self):
        response = self.app.post('/alunos', json={
            "nome": 456, "data_nascimento": "2005-05-15", "nota1": 8.5, "nota2": 9.0
        })
        self.assertEqual(response.status_code, 400)

    def test_get_professor_com_idade(self):
        response = self.app.get('/professores')
        self.assertEqual(response.status_code, 200)
        professores = response.json
        for professor in professores:
            self.assertIn("idade", professor)

    def test_nome_sem_caracteres_especiais(self):
        response = self.app.post('/alunos', json={
            "nome": "João@#", "data_nascimento": "2005-05-15", "nota_primeiro_semestre": 8.5, "nota_segundo_semestre": 9.0
        })
        self.assertEqual(response.status_code, 400)

        response = self.app.post('/professores', json={
            "nome": "Dr. *Roberto*", "disciplina": "Química", "data_nascimento": "1975-09-23", "salario": 4500.00,  "email": "joao@email.com"
        })
        self.assertEqual(response.status_code, 400)

        response = self.app.post('/turmas', json={
            "nome": "Turma!A", "turno": "Manhã", "capacidade": 25
        })
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
