from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_cors import CORS

from src.unidade_prisional import ListarUnidades, BuscarUnidades, CriarUnidades, AlterarUnidades, RemoverUnidades
from src.pavilhao import ListarPavilhoes, BuscarPavilhoes, CriarPavilhoes, AlterarPavilhoes, RemoverPavilhoes
from src.bloco import ListarBlocos, BuscarBlocos, CriarBlocos, AlterarBlocos, RemoverBlocos
from src.cela import ListarCelas, BuscarCelas, CriarCelas, AlterarCelas, RemoverCelas
from src.servidor import ListarServidores, BuscarServidores, CriarServidores, AlterarServidores, RemoverServidores

app = Flask(__name__)
api = Api(app)
CORS(app)

class Index(Resource):
	def get(self):
		return "Index"

api.add_resource(Index, '/')
api.add_resource(ListarUnidades, '/unidades/listar')
api.add_resource(BuscarUnidades, '/unidades/buscar/<int:codigo>')
api.add_resource(CriarUnidades, '/unidades/criar')
api.add_resource(AlterarUnidades, '/unidades/alterar')
api.add_resource(RemoverUnidades, '/unidades/remover')

api.add_resource(ListarBlocos, '/blocos/listar')
api.add_resource(BuscarBlocos, '/blocos/buscar')
api.add_resource(CriarBlocos, '/blocos/criar')
api.add_resource(AlterarBlocos, '/blocos/alterar')
api.add_resource(RemoverBlocos, '/blocos/remover')

api.add_resource(ListarCelas, '/celas/listar')
api.add_resource(BuscarCelas, '/celas/buscar')
api.add_resource(CriarCelas, '/celas/criar')
api.add_resource(AlterarCelas, '/celas/alterar')
api.add_resource(RemoverCelas, '/celas/remover')

api.add_resource(ListarPavilhoes, '/pavilhoes/listar')
api.add_resource(BuscarPavilhoes, '/pavilhoes/buscar')
api.add_resource(CriarPavilhoes, '/pavilhoes/criar')
api.add_resource(AlterarPavilhoes, '/pavilhoes/alterar')
api.add_resource(RemoverPavilhoes, '/pavilhoes/remover')

api.add_resource(ListarServidores, '/servidores/listar')
api.add_resource(BuscarServidores, '/servidores/buscar')
api.add_resource(CriarServidores, '/servidores/criar')
api.add_resource(AlterarServidores, '/servidores/alterar')
api.add_resource(RemoverServidores, '/servidores/remover')

if __name__ == "__main__":
	app.run(debug=True)