from flask_restx import Api

api = Api(
    title='API de Gestão Escolar',
    version='1.0',
    description='Documentação da API para gerenciamento de alunos, professores e turmas.',
    doc='/docs',
    mask_swagger=False, 
)
