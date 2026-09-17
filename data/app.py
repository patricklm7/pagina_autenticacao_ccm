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
# CSS DA PÁGINA PRINCIPAL
# ==========================================

@app.route("/style.css")
def css():

    return send_from_directory("..", "style.css")


# ==========================================
# PAINEL ADMINISTRATIVO
# ==========================================

@app.route("/admin")
def admin():

    return send_from_directory("..", "admin.html")


# ==========================================
# CSS DO PAINEL
# ==========================================

@app.route("/admin.css")
def admin_css():

    return send_from_directory("..", "admin.css")


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
# BUSCAR REGISTROS
# ==========================================

@app.route("/registros")
def registros():

    conexao = sqlite3.connect("banco.db")

    cursor = conexao.cursor()


    cursor.execute("""
        SELECT
            id,
            email,
            serie,
            turma,
            equipamento,
            data,
            horario

        FROM registros

        ORDER BY id DESC
    """)


    registros_banco = cursor.fetchall()

    conexao.close()


    lista = []


    for registro in registros_banco:

        lista.append({

            "id": registro[0],

            "email": registro[1],

            "serie": registro[2],

            "turma": registro[3],

            "equipamento": registro[4],

            "data": registro[5],

            "horario": registro[6]

        })


    return jsonify({

        "registros": lista

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