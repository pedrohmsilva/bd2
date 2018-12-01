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
			return unidade

		resultado = []
		for data in unidades['data']:
			resultado.append(Util.formatResponse(data, unidades['columns'], ['endereco.']))

		for i in range(len(resultado)):
			resultado[i]['num'] = resultado[i]['numero']
			del resultado[i]['numero']
		
		return resultado

class BuscarUnidades(Resource):

	def get(self):
		conn = Connection()

		codigo = str(request.args['codigo'])

		unidade = conn.query("select " + Util.formatQuery('up', 'up') + ", " + Util.formatQuery('up.endereco', 'endereco') + " from unidades_prisionais up where codigo = " + codigo)

		if(unidade['success'] == False):
			return unidade

		resultado = []
		for data in unidade['data']:
			resultado.append(Util.formatResponse(data, unidade['columns'], ['endereco.']))
		
		for i in range(len(resultado)):
			resultado[i]['num'] = resultado[i]['numero']
			del resultado[i]['numero']
		
		return resultado

class CriarUnidades(Resource):

	def post(self):
		conn = Connection()

		unidade = {}
		unidade['codigo'] = str(request.json['codigo'])
		unidade['nome'] = "'" + request.json['nome'] + "'"

		endereco = {}
		endereco['tipo_logadouro'] = "'" + request.json['tipo_logadouro'] + "'"
		endereco['logradouro'] = "'" + request.json['logradouro'] + "'"
		endereco['numero'] = "'" + request.json['numero'] + "'"
		endereco['bairro'] = "'" + request.json['bairro'] + "'"
		endereco['cidade'] = "'" + request.json['cidade'] + "'"
		endereco['uf'] = "'" + request.json['uf'] + "'"
		endereco['cep'] = "'" + request.json['cep'] + "'"


		command = (
			"insert into unidades_prisionais values ("
				"Unidade_Prisional_TY (" +
					unidade['codigo'] + "," +
					unidade['nome'] + "," +
					"Endereco_TY (" +
						endereco['tipo_logadouro'] + "," +
						endereco['logradouro'] + "," +
						endereco['numero'] + "," +
						endereco['bairro'] + "," +
						endereco['cidade'] + "," +
						endereco['uf'] + "," +
						endereco['cep'] +
					")"
				")"
			")")

		return conn.update(command)

class AlterarUnidades(Resource):

	def post(self):
		conn = Connection()

		unidade = {}
		unidade['codigo'] = str(request.json['codigo'])
		unidade['nome'] = Util.formatString(request.json['nome'])
		unidade['tipo_logadouro'] = Util.formatString(request.json['tipo_logradouro'])
		unidade['logradouro'] = Util.formatString(request.json['logradouro'])
		unidade['numero'] = Util.formatString(request.json['numero'])
		unidade['bairro'] = Util.formatString(request.json['bairro'])
		unidade['cidade'] = Util.formatString(request.json['cidade'])
		unidade['uf'] = Util.formatString(request.json['uf'])
		unidade['cep'] = Util.formatString(request.json['cep'])

		command = (
			"update unidades_prisionais up set " +
				"up.nome = " + unidade['nome'] + ", " +
				"up.endereco.tipo_logadouro = " + unidade['tipo_logadouro'] + ", " +
				"up.endereco.logradouro = " + unidade['logradouro'] + ", " +
				"up.endereco.numero = " + unidade['numero'] + ", " +
				"up.endereco.bairro = " + unidade['bairro'] + ", " +
				"up.endereco.cidade = " + unidade['cidade'] + ", " +
				"up.endereco.uf = " + unidade['uf'] + ", " +
				"up.endereco.cep = " + unidade['cep'] +
			" where up.codigo = " + unidade['codigo']
		)

		return conn.update(command)

class RemoverUnidades(Resource):

	def post(self):
		conn = Connection()

		return conn.update("delete from unidades_prisionais where codigo = " + str(request.json["codigo"]))

