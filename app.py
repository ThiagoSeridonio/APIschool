from controller.professores_rotas import prof_rotas
from controller.alunos_rotas import alunos_rotas
from controller.turmas_rotas import turmas_rotas
from config import app, db

app.register_blueprint(prof_rotas)
app.register_blueprint(alunos_rotas)
app.register_blueprint(turmas_rotas)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
