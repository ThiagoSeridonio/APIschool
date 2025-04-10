import unittest
import json
from app import app


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Simulação do conteúdo inicial do database.json
        self.mock_db_data = {
            "professores": [],
            "alunos": [],
            "turmas": []
        }

        mock_file_data = json.dumps(self.mock_db_data)

        self.patcher = patch(
            "builtins.open", mock_open(read_data=mock_file_data))
        self.mock_open = self.patcher.start()

        self.mock_open.return_value.__enter__.return_value.write = lambda s: None

    def tearDown(self):
        self.patcher.stop()

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
            "salario": 5000.0
        }
        response = self.app.post("/professores", json=novo_professor)
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
        nova_turma = {
            "nome": "Turma A",
            "turno": "Manhã",
            "capacidade": 30
        }
        response = self.app.post("/turmas", json=nova_turma)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json)

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
            "nota_primeiro_semestre": 8.5,
            "nota_segundo_semestre": 9.0
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
            "nome": 123, "disciplina": "Matemática", "data_nascimento": "1980-12-01", "salario": 3000.50
        })
        self.assertEqual(response.status_code, 400)

    def test_nome_e_data_nascimento_aluno(self):
        response = self.app.post('/alunos', json={
            "nome": 456, "data_nascimento": "2005-05-15", "nota_primeiro_semestre": 8.5, "nota_segundo_semestre": 9.0
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
            "nome": "Dr. *Roberto*", "disciplina": "Química", "data_nascimento": "1975-09-23", "salario": 4500.00
        })
        self.assertEqual(response.status_code, 400)

        response = self.app.post('/turmas', json={
            "nome": "Turma!A", "turno": "Manhã", "capacidade": 25
        })
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
