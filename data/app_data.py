from flask import Flask, send_from_directory, request, jsonify
import sqlite3
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
BANCO = BASE_DIR / "banco.db"


# ==========================================
# CRIAR BANCO
# ==========================================

def criar_banco():

    conexao = sqlite3.connect(BANCO)

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
# PÁGINA PRINCIPAL
# ==========================================

@app.route("/")
def inicio():

    return send_from_directory(BASE_DIR, "index.html")


# ==========================================
# CSS
# ==========================================

@app.route("/style.css")
def css():

    return send_from_directory(BASE_DIR, "style.css")


# ==========================================
# PAINEL ADMINISTRATIVO
# ==========================================

@app.route("/admin")
def admin():

    return send_from_directory(BASE_DIR, "admin.html")


# ==========================================
# CSS DO ADMIN
# ==========================================

@app.route("/admin.css")
def admin_css():

    return send_from_directory(BASE_DIR, "admin.css")


# ==========================================
# REGISTRAR
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

    conexao = sqlite3.connect(BANCO)

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

    print("========== NOVO REGISTRO ==========")
    print("E-mail:", email)
    print("Série:", serie)
    print("Turma:", turma)
    print("Equipamento:", equipamento)
    print("Data:", data)
    print("Horário:", horario)
    print("===================================")

    return jsonify({
        "sucesso": True,
        "mensagem": "Registro realizado com sucesso!"
    })


# ==========================================
# BUSCAR REGISTROS
# ==========================================

@app.route("/registros")
def registros():

    conexao = sqlite3.connect(BANCO)

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