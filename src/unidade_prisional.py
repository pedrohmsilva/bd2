from flask import Flask, request, jsonify
from flask_restful import Resource, Api

import sys
sys.path.insert(0, '..')
from Connection import Connection
from util import Util

app = Flask(__name__)
api = Api(app)

class ListarUnidades(Resource):

	def get(self):
		conn = Connection()
		unidades = conn.query("select " + Util.formatQuery('up', 'up') + ", " + Util.formatQuery('up.endereco', 'endereco') + " from unidades_prisionais up")

		if (unidades['success'] == False):
			return unidades

		resultado = []
		for data in unidades['data']:
			resultado.append(Util.formatResponse(data, unidades['columns'], ['endereco.']))
		
		return {
			"success": True,
			"data": resultado
		}

class BuscarUnidades(Resource):

	def get(self, codigo):
		conn = Connection()
		unidade = conn.query("select " + Util.formatQuery('up', 'up') + ", " + Util.formatQuery('up.endereco', 'endereco') + " from unidades_prisionais up where codigo = " + str(codigo))

		if(unidade['success'] == False):
			return unidade

		resultado = []
		for data in unidade['data']:
			resultado.append(Util.formatResponse(data, unidade['columns'], ['endereco.']))
		
		return {
			"success": True,
			"data": resultado
		}