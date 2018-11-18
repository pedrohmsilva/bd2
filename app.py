from flask import Flask, jsonify, request
from flask_restful import Resource, Api

from src.unidade_prisional import ListarUnidades, BuscarUnidades
from src.pavilhao import ListarPavilhoes, BuscarPavilhoes, CriarPavilhoes, AlterarPavilhoes, RemoverPavilhoes

app = Flask(__name__)
api = Api(app)

class Index(Resource):
	def get(self):
		return "Index"

api.add_resource(Index, '/')
api.add_resource(ListarUnidades, '/unidades/listar')
api.add_resource(BuscarUnidades, '/unidades/buscar/<int:codigo>')
api.add_resource(ListarPavilhoes, '/pavilhoes/listar')
api.add_resource(BuscarPavilhoes, '/pavilhoes/buscar')
api.add_resource(CriarPavilhoes, '/pavilhoes/criar')
api.add_resource(AlterarPavilhoes, '/pavilhoes/alterar')
api.add_resource(RemoverPavilhoes, '/pavilhoes/remover')

if __name__ == "__main__":
	app.run(debug=True)