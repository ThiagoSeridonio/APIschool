import json
import os
import uuid


class Database:
    DB_FILE = "database.json"

    @staticmethod
    def load_data():
        if not os.path.exists(Database.DB_FILE):
            with open(Database.DB_FILE, "w") as db:
                json.dump({"professores": [], "turmas": [], "alunos": []}, db)

        with open(Database.DB_FILE, "r") as db:
            return json.load(db)

    @staticmethod
    def save_data(data):
        with open(Database.DB_FILE, "w", encoding="utf-8") as db_file:
            json.dump(data, db_file, indent=4, ensure_ascii=False)

    @staticmethod
    def gerar_uuid():
        return str(uuid.uuid4())


