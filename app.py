from flask import Flask, jsonify, request
from flask_restful import Resource, Api

import src.unidade_prisional as unidade_prisional
from src.pavilhao import ListarPavilhoes, BuscarPavilhoes, CriarPavilhoes, AlterarPavilhoes, RemoverPavilhoes

app = Flask(__name__)
api = Api(app)

class Index(Resource):
	def get(self):
		return "Index"

api.add_resource(Index, '/')
api.add_resource(unidade_prisional.Listar, '/unidades/listar')
api.add_resource(unidade_prisional.Buscar, '/unidades/<int:unidade>')
api.add_resource(ListarPavilhoes, '/pavilhoes/listar')
api.add_resource(BuscarPavilhoes, '/pavilhoes/buscar')
api.add_resource(CriarPavilhoes, '/pavilhoes/criar')
api.add_resource(AlterarPavilhoes, '/pavilhoes/alterar')
api.add_resource(RemoverPavilhoes, '/pavilhoes/remover')

if __name__ == "__main__":
	app.run(debug=True)