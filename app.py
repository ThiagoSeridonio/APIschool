from professores.professores_rotas import prof_rotas
from alunos.alunos_rotas import alunos_rotas
from turmas.turmas_rotas import turmas_rotas
from config import app
from flask import Flask, jsonify, request
import database as db
import datetime
import re

app.register_blueprint(prof_rotas)
app.register_blueprint(alunos_rotas)
app.register_blueprint(turmas_rotas)

if __name__ == '__main__':
    app.run(debug=True)
