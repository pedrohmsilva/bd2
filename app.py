from flask import Flask, jsonify, request
from flask_restful import Resource, Api

from src.unidade_prisional import ListarUnidades, BuscarUnidades

app = Flask(__name__)
api = Api(app)

class Index(Resource):
	def get(self):
		return "Index"

api.add_resource(Index, '/')
api.add_resource(ListarUnidades, '/unidades/listar')
api.add_resource(BuscarUnidades, '/unidades/buscar/<int:codigo>')

if __name__ == "__main__":
	app.run(debug=True)