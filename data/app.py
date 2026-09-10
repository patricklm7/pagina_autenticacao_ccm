from flask import Flask, send_from_directory, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)


# ==========================================
# PÁGINA PRINCIPAL
# ==========================================

@app.route("/")
def inicio():

    return send_from_directory("..", "index.html")


# ==========================================
# CSS
# ==========================================

@app.route("/style.css")
def css():

    return send_from_directory("..", "style.css")


# ==========================================
# CRIAR BANCO DE DADOS
# ==========================================

def criar_banco():

    conexao = sqlite3.connect("banco.db")

    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            email TEXT,

            serie TEXT,

            turma TEXT,

            equipamento TEXT,

            data TEXT,

            horario TEXT

        )
    """)

    conexao.commit()

    conexao.close()


# ==========================================
# REGISTRAR USUÁRIO
# ==========================================

@app.route("/registrar", methods=["POST"])
def registrar():

    dados = request.json

    email = dados["email"]
    serie = dados["serie"]
    turma = dados["turma"]
    equipamento = dados["equipamento"]

    agora = datetime.now()

    data = agora.strftime("%d/%m/%Y")
    horario = agora.strftime("%H:%M:%S")


    print("========== NOVO REGISTRO ==========")
    print("E-mail:", email)
    print("Série:", serie)
    print("Turma:", turma)
    print("Equipamento:", equipamento)
    print("Data:", data)
    print("Horário:", horario)
    print("===================================")


    conexao = sqlite3.connect("banco.db")

    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO registros
        (email, serie, turma, equipamento, data, horario)

        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        email,
        serie,
        turma,
        equipamento,
        data,
        horario
    ))

    conexao.commit()

    conexao.close()


    return jsonify({
        "sucesso": True,
        "mensagem": "Registro realizado com sucesso!"
    })


# ==========================================
# INICIAR SERVIDOR
# ==========================================

if __name__ == "__main__":

    criar_banco()

    app.run(
        host="0.0.0.0",
        port=5000
    )