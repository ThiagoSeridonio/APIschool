from controller.professores_rotas import prof_rotas
from controller.alunos_rotas import alunos_rotas
from controller.turmas_rotas import turmas_rotas
from config import app, db
import os

app.register_blueprint(prof_rotas)
app.register_blueprint(alunos_rotas)
app.register_blueprint(turmas_rotas)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
