import unittest
import json
from app import app  # Importa o objeto `app` do arquivo principal


class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()  # Configura o cliente de teste do Flask
        self.app.testing = True

    # Teste para verificar se nome e data de nascimento dos alunos e professores são strings no POST e PUT
    def test_nome_e_data_nascimento_professor(self):
        response = self.app.post('/professores', json={
            "nome": 123, "disciplina": "Matemática", "data_nascimento": '1980-12-01', "salario": 3000.50
        })
        self.assertEqual(response.status_code, 400)

    def test_nome_e_data_nascimento_aluno(self):
        response = self.app.post('/alunos', json={
            "nome": 456, "data_nascimento": '2005-05-15', "nota_primeiro_semestre": 8.5, "nota_segundo_semestre": 9.0
        })
        self.assertEqual(response.status_code, 400)

    # Teste para verificar se a idade do professor é retornada corretamente no GET
    def test_get_professor_com_idade(self):
        response = self.app.get('/professores')
        self.assertEqual(response.status_code, 200)
        professores = json.loads(response.data)
        for professor in professores:
            self.assertIn("idade", professor)

    # Teste para verificar se o salário dos professores é float no POST e PUT
    def test_salario_professor(self):
        response = self.app.post('/professores', json={
            "nome": "Carlos", "disciplina": "Física", "data_nascimento": "1985-07-20", "salario": "cinco mil"
        })
        self.assertEqual(response.status_code, 400)

    # Teste para verificar se o nome e turno da turma são strings no POST e PUT
    def test_nome_e_turno_turma(self):
        response = self.app.post('/turmas', json={
            "nome": 123, "turno": 456, "capacidade": 30
        })
        self.assertEqual(response.status_code, 400)

    # Teste para verificar chamadas de aluno, professor ou turma por ID inexistente
    def test_get_aluno_inexistente(self):
        response = self.app.get('/alunos/999')
        self.assertEqual(response.status_code, 404)

    def test_get_professor_inexistente(self):
        response = self.app.get('/professores/999')
        self.assertEqual(response.status_code, 404)

    def test_get_turma_inexistente(self):
        response = self.app.get('/turmas/999')
        self.assertEqual(response.status_code, 404)

    # Teste para verificar se o GET dos alunos retorna a data de nascimento e média final
    def test_get_alunos_com_data_media_e_idade(self):
        response = self.app.get('/alunos')
        self.assertEqual(response.status_code, 200)
        alunos = json.loads(response.data)
        for aluno in alunos:
            self.assertIn("media_final", aluno)
            self.assertIn("data_nascimento", aluno)

    # Testes para verificar se nenhum campo está vazio em POST e PUT
    def test_campos_nao_vazios_post_aluno(self):
        response = self.app.post('/alunos', json={
            "nome": "", "data_nascimento": "", "nota_primeiro_semestre": None, "nota_segundo_semestre": None
        })
        self.assertEqual(response.status_code, 400)

    def test_campos_nao_vazios_post_professor(self):
        response = self.app.post('/professores', json={
            "nome": "", "disciplina": "", "data_nascimento": "", "salario": None
        })
        self.assertEqual(response.status_code, 400)

    def test_campos_nao_vazios_post_turma(self):
        response = self.app.post('/turmas', json={
            "nome": "", "turno": "", "capacidade": None
        })
        self.assertEqual(response.status_code, 400)

    def test_campos_nao_vazios_put_aluno(self):
        response = self.app.put('/alunos/1', json={
            "nome": "", "data_nascimento": "", "nota_primeiro_semestre": None, "nota_segundo_semestre": None
        })
        self.assertEqual(response.status_code, 400)

    def test_campos_nao_vazios_put_professor(self):
        response = self.app.put('/professores/1', json={
            "nome": "", "disciplina": "", "data_nascimento": "", "salario": None
        })
        self.assertEqual(response.status_code, 400)

    def test_campos_nao_vazios_put_turma(self):
        response = self.app.put('/turmas/1', json={
            "nome": "", "turno": "", "capacidade": None
        })
        self.assertEqual(response.status_code, 400)

    # Teste para verificar se nomes não contêm caracteres especiais
    def test_nome_sem_caracteres_especiais(self):
        response = self.app.post('/alunos', json={
            "nome": "João@#", "data_nascimento": "2005-05-15", "nota_primeiro_semestre": 8.5,
            "nota_segundo_semestre": 9.0
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
