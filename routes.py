# Importa o Flask e o model
from flask import Flask, jsonify, request
from flask_cors import CORS
from models import Materia

# Instancia a aplicação Flask e o model
app = Flask(__name__)
CORS(app)
materiaModel = Materia()

# Rota raiz => retorna todas as matérias como um JSON
# GET => retorna [{"materia": "Matéria", "tipo": "Tipo"}, {...}, ...]
@app.route("/")
def getMaterias():
    order_by = request.args.get("order_by")

    if order_by:
        if order_by == "materia":
            materias = materiaModel.get(order_by="materia")
        elif order_by == "tipo":
            materias = materiaModel.get(order_by="tipo")
    else:
        materias = materiaModel.get()

    return jsonify(materias)

# Rota /create => aceita requisições POST em formato JSON; cria uma matéria.
# POST => {"materia": "Nome da matéria", "tipo": "Tipo de matéria (se é humana, exata...)"}
@app.route("/create", methods=["POST"])
def createMateria():
    req = request.get_json()
    materia = req["materia"]
    tipo = req["tipo"]

    materiaModel.create(materia, tipo)

    return jsonify({"status": "OK"})

# Rota /update => aceita requisições PUT em formato JSON; atualiza uma matéria já existente.
# PUT => {
#          "materiaToUpdate": "Matéria existente a ser atualizada",
#          "newMateria": "Novo nome de matéria",
#          "newTipo": "Novo tipo de matéria"
#        }
@app.route("/update", methods=["PUT"])
def updateMateria():
    req = request.get_json()
    materiaToUpdate = req["materiaToUpdate"]
    newMateria = req["newMateria"]
    newTipo = req["newTipo"]

    materiaModel.update(materiaToUpdate, newMateria, newTipo)

    return jsonify({"status": "OK"})

# Rota /delete/(nome da matéria) => aceita requisições DELETE; deleta uma matéria do banco de dados.
# DELETE => /delete/Matemática (deleta a matéria "Matemática")
@app.route("/delete/<materia>", methods=["DELETE"])
def deleteMateria(materia):
    materiaModel.delete(materia)

    return jsonify({"status": "OK"})

if __name__ == "__main__":
    app.run(debug=True)
